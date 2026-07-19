#!/usr/bin/env node
/**
 * Embedding pipeline for the page visualizations.
 *
 * Scans the prerendered HTML in build/, embeds each page's sentences with
 * Qwen3-Embedding-0.6B (transformers.js, ONNX — the model downloads once and
 * is cached), reduces them to 3D with UMAP (seeded, deterministic), and writes
 * static/embeddings.json: per page the node coordinates, similarity edges and
 * a content hue, consumed by src/lib/visualization.js and the og card
 * backgrounds.
 *
 * Edges are the strongest EDGE_FRACTION of sentence pairs — relative
 * selection, so graph density survives embedding-model swaps (absolute
 * cosine thresholds are not comparable between models). Raw sentence
 * vectors are cached in .cache/embeddings.json (gitignored, keyed by
 * model + sentence hash) so re-tuning UMAP/edges skips the model run.
 *
 * Run after `pnpm build` (the npm script also rebuilds, so build/ picks up
 * the fresh JSON and cards):
 *
 *     pnpm build && pnpm generate-embeddings
 */
import { createHash } from 'node:crypto';
import { mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, sep } from 'node:path';
import { parseArgs } from 'node:util';
import { parse } from 'node-html-parser';
import { pipeline } from '@huggingface/transformers';
import { UMAP } from 'umap-js';

// Block-level HTML elements (text chunks split at these boundaries).
const BLOCK_TAGS = new Set([
  'address', 'article', 'aside', 'blockquote', 'details', 'div', 'dl', 'dd',
  'fieldset', 'figcaption', 'figure', 'footer', 'form', 'h1', 'h2', 'h3', 'h4',
  'h5', 'h6', 'header', 'hgroup', 'hr', 'li', 'main', 'nav', 'ol', 'p', 'pre',
  'section', 'summary', 'table', 'ul'
]);

// Elements skipped entirely (non-content).
const SKIP_TAGS = new Set(['script', 'style', 'nav', 'header', 'footer', 'aside', 'head', 'meta']);

// Minimum sentence length (characters) to keep.
const MIN_SENTENCE_LENGTH = 10;

// Fraction of strongest sentence pairs kept as edges. Relative selection
// keeps graph density stable across embedding models; absolute cosine
// thresholds are not comparable between models (MiniLM spreads similarities
// over ~0-0.8, Qwen3 compresses them into ~0.2-0.75).
const EDGE_FRACTION = 0.015;

// Raw sentence vectors cached here (keyed by model + sentence hash) so
// re-tuning the layout or edges doesn't re-run the model.
const CACHE_PATH = '.cache/embeddings.json';

// Embedding model (1024 dimensions). Qwen3-Embedding-0.6B scores 64.3 on the
// MTEB multilingual leaderboard vs ~59 for all-MiniLM-L6-v2, at a still-modest
// size; q8 keeps the download ~600 MB and CPU inference fast.
const MODEL_NAME = 'onnx-community/Qwen3-Embedding-0.6B-ONNX';

// Extract text chunks from HTML, respecting block structure.
function extractChunks(root) {
  const chunks = [];
  let current = '';
  const flush = () => {
    const text = current.trim();
    if (text) chunks.push(text);
    current = '';
  };
  const walk = (node) => {
    if (node.nodeType === 3) {
      // TextNode.text decodes HTML entities; doctype parses as a text node.
      if (!node.rawText.trimStart().startsWith('<!')) current += node.text;
      return;
    }
    if (node.nodeType !== 1) return;
    const tag = node.tagName?.toLowerCase(); // parse() root has no tagName
    if (tag && SKIP_TAGS.has(tag)) return;
    const isBlock = tag != null && BLOCK_TAGS.has(tag);
    if (isBlock) flush();
    node.childNodes.forEach(walk);
    if (isBlock) flush();
  };
  walk(root);
  flush();
  return chunks;
}

// Naive sentence split: terminal punctuation followed by whitespace. Chunks
// without punctuation (headings, list items) stay whole.
function splitSentences(text) {
  return text.replace(/\s+/g, ' ').match(/[^.!?]+[.!?]+(?=\s|$)|[^.!?]+$/g) ?? [];
}

function htmlToSentences(html) {
  return extractChunks(parse(html))
    .flatMap(splitSentences)
    .map((s) => s.trim())
    .filter((s) => s.length >= MIN_SENTENCE_LENGTH);
}

// Embed sentences; vectors come out L2-normalized, so dot product == cosine
// similarity and UMAP's euclidean metric is equivalent to cosine. Qwen3
// embedding models pool at the final EOS token, not the mean. Vectors are
// cached by model + sentence hash; only misses hit the model.
async function embedSentences(extractor, sentences, cache) {
  const vectors = new Array(sentences.length);
  const missing = [];
  for (let i = 0; i < sentences.length; i++) {
    const hit = cache.get(cacheKey(sentences[i]));
    if (hit) vectors[i] = hit;
    else missing.push(i);
  }
  if (missing.length > 0) {
    const output = await extractor(
      missing.map((i) => sentences[i]),
      { pooling: 'last_token', normalize: true }
    );
    const fresh = output.tolist();
    missing.forEach((i, n) => {
      vectors[i] = fresh[n];
      cache.set(cacheKey(sentences[i]), fresh[n]);
    });
  }
  return vectors;
}

function cacheKey(sentence) {
  return createHash('sha256').update(MODEL_NAME + '\0' + sentence).digest('hex');
}

function loadCache() {
  try {
    return new Map(Object.entries(JSON.parse(readFileSync(CACHE_PATH, 'utf8'))));
  } catch {
    return new Map();
  }
}

function saveCache(cache) {
  mkdirSync(dirname(CACHE_PATH), { recursive: true });
  writeFileSync(CACHE_PATH, JSON.stringify(Object.fromEntries(cache)));
}

// Deterministic PRNG for UMAP's random initialization/sampling.
function mulberry32(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// Reduce embeddings to 3D with UMAP, normalized to 0-1 per dimension.
function reduceTo3D(vectors, { nNeighbors = 15, minDist = 0.1 } = {}) {
  if (vectors.length < 2) return [[0.5, 0.5, 0.5]];
  const umap = new UMAP({
    nComponents: 3,
    nNeighbors: Math.min(nNeighbors, vectors.length - 1),
    minDist,
    random: mulberry32(42)
  });
  const coords = umap.fit(vectors);
  const mins = [Infinity, Infinity, Infinity];
  const maxs = [-Infinity, -Infinity, -Infinity];
  for (const c of coords) {
    for (let i = 0; i < 3; i++) {
      mins[i] = Math.min(mins[i], c[i]);
      maxs[i] = Math.max(maxs[i], c[i]);
    }
  }
  return coords.map((c) => c.map((v, i) => (v - mins[i]) / (maxs[i] - mins[i] || 1)));
}

// Keep the strongest `fraction` of pairs as edges, normalized to a 0-1
// strength for rendering. Deterministic: ties broken by node indices.
function computeEdges(vectors, { fraction = EDGE_FRACTION } = {}) {
  const pairs = [];
  for (let i = 0; i < vectors.length; i++) {
    for (let j = i + 1; j < vectors.length; j++) {
      let similarity = 0;
      for (let k = 0; k < vectors[i].length; k++) similarity += vectors[i][k] * vectors[j][k];
      pairs.push({ source: i, target: j, similarity });
    }
  }
  pairs.sort(
    (a, b) => b.similarity - a.similarity || a.source - b.source || a.target - b.target
  );
  const edges = pairs.slice(0, Math.round(pairs.length * fraction));
  const max = edges[0]?.similarity ?? 0;
  const min = edges[edges.length - 1]?.similarity ?? max;
  return edges.map(({ source, target, similarity }) => ({
    source,
    target,
    strength: max > min ? (similarity - min) / (max - min) : 1
  }));
}

// Derive a well-distributed hue (0-360) from the mean embedding.
function contentHue(vectors) {
  const dim = vectors[0].length;
  const mean = new Float64Array(dim);
  for (const v of vectors) {
    for (let k = 0; k < dim; k++) mean[k] += v[k] / vectors.length;
  }
  const hex = createHash('sha256').update(Buffer.from(mean.buffer)).digest('hex');
  return parseInt(hex.slice(0, 8), 16) % 360;
}

async function visualizationData(sentences, extractor, cache) {
  if (sentences.length === 0) return { nodes: [], edges: [], hue: 0 };
  const vectors = await embedSentences(extractor, sentences, cache);
  const coords = reduceTo3D(vectors);
  return {
    nodes: sentences.map((text, i) => ({
      id: i,
      x: coords[i][0],
      y: coords[i][1],
      z: coords[i][2],
      text,
      position: i / Math.max(sentences.length - 1, 1)
    })),
    edges: computeEdges(vectors),
    hue: contentHue(vectors)
  };
}

// Find index.html files under the input dir and derive their keys:
// index.html -> home, articles/<slug>/index.html -> articles/<slug>.
// The articles index page is skipped: the `articles` key below holds the
// combined scatter of all articles instead.
function discoverPages(inputDir) {
  return readdirSync(inputDir, { recursive: true })
    .map((file) => file.split(sep).join('/'))
    .filter((file) => file === 'index.html' || file.endsWith('/index.html'))
    .sort()
    .map((file) => ({
      key: file === 'index.html' ? 'home' : file.slice(0, -'/index.html'.length),
      path: join(inputDir, file)
    }))
    .filter(({ key }) => key !== 'articles');
}

async function main() {
  const { values } = parseArgs({
    options: {
      input: { type: 'string', default: 'build' },
      output: { type: 'string', default: 'static/embeddings.json' }
    }
  });

  const pages = discoverPages(values.input);
  if (pages.length === 0) {
    console.error(`No index.html files found under ${values.input} — run \`pnpm build\` first.`);
    process.exitCode = 1;
    return;
  }

  const extractor = await pipeline('feature-extraction', MODEL_NAME, { dtype: 'q8' });
  const cache = loadCache();

  const sentencesByKey = new Map();
  const result = {};
  for (const { key, path } of pages) {
    const sentences = htmlToSentences(readFileSync(path, 'utf8'));
    sentencesByKey.set(key, sentences);
    result[key] = await visualizationData(sentences, extractor, cache);
    console.error(
      `${key}: ${result[key].nodes.length} nodes, ${result[key].edges.length} edges, hue ${result[key].hue}`
    );
  }

  // Combined scatter of all article sentences: background for /og/articles.png.
  const articleSentences = [...sentencesByKey.entries()]
    .filter(([key]) => key.startsWith('articles/'))
    .sort()
    .flatMap(([, sentences]) => sentences);
  if (articleSentences.length > 0) {
    result.articles = await visualizationData(articleSentences, extractor, cache);
    console.error(
      `articles (combined): ${result.articles.nodes.length} nodes, ${result.articles.edges.length} edges, hue ${result.articles.hue}`
    );
  }

  saveCache(cache);

  mkdirSync(dirname(values.output), { recursive: true });
  writeFileSync(values.output, JSON.stringify(result, null, 2) + '\n');
  console.error(`Wrote ${values.output}`);
}

await main();

// Social-card renderer for the og:* endpoints. A card is a simplified take
// on the page hero: the page's sentence-embedding scatter (static/embeddings.json,
// the same data src/lib/visualization.js renders) zoomed in to a few large
// nodes, the hero's radial backdrop blur at the center, and the "Resolve."
// wordmark (pre-baked glyph paths, see wordmark.svg). The SVG is serialized by
// hand and rasterized by resvg — no text layout or font handling at build
// time.
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { Resvg } from '@resvg/resvg-js';

// The wordmark's outer <svg> root is stripped: a nested <svg> would clip the
// glow (filter region extends well past the wordmark's viewport).
const WORDMARK = readFileSync(join(process.cwd(), 'src/lib/server/wordmark.svg'), 'utf8')
  .replace(/^<svg[^>]*>/, '')
  .replace(/<\/svg>\s*$/, '');

const WIDTH = 1200;
const HEIGHT = 630;
const LIGHT = '#fafafa'; // --color-light
const EDGE = '#d5d5d5'; // .visualization line

// The hero's ::before backdrop (styles.css): brightness(1.2) blur() under a
// radial-gradient mask, fading out from the center. Mirrored here by drawing
// the scatter twice — sharp, then a brightened/blurred copy visible only
// through a radial mask (SVG masks are luminance: white shows, black reveals
// the sharp copy underneath). More pronounced than the hero's: cards are
// viewed as small thumbnails, where subtle blur reads as noise.
const SOFTEN_DEFS = `<defs>
  <radialGradient id="og-fade">
    <stop offset="50%" stop-color="#fff"/>
    <stop offset="100%" stop-color="#000"/>
  </radialGradient>
  <mask id="og-fade-mask" maskUnits="userSpaceOnUse">
    <rect width="${WIDTH}" height="${HEIGHT}" fill="url(#og-fade)"/>
  </mask>
  <filter id="og-soften">
    <feGaussianBlur stdDeviation="10"/>
    <feComponentTransfer>
      <feFuncR type="linear" slope="1.2"/>
      <feFuncG type="linear" slope="1.2"/>
      <feFuncB type="linear" slope="1.2"/>
    </feComponentTransfer>
  </filter>
</defs>`;

// Zoom of the scatter relative to the homepage hero's sizing: at 2 the card
// shows a crop of the hero-scale scatter — few nodes, large.
const ZOOM = 2;

let embeddings = {};
try {
  embeddings = JSON.parse(readFileSync(join(process.cwd(), 'static/embeddings.json'), 'utf8'));
} catch {
  // Cards still render (wordmark only) when embeddings haven't been generated yet.
}

// hsl() -> hex; s and l in 0..1.
function hslHex(h, s, l) {
  h = (((h % 360) + 360) % 360) / 30;
  const a = s * Math.min(l, 1 - l);
  const channel = (n) => {
    const c = l - a * Math.max(-1, Math.min((n + h) % 12 - 3, 9 - ((n + h) % 12), 1));
    return Math.round(255 * c).toString(16).padStart(2, '0');
  };
  return `#${channel(0)}${channel(8)}${channel(4)}`;
}

const num = (v) => Math.round(v * 100) / 100;

function scatterShapes(data) {
  const base = Math.max(WIDTH, HEIGHT) * 1.05 * ZOOM;
  const stroke = base * 0.0012;
  const minRadius = base * 0.0075;
  const maxRadius = base * 0.025;
  const padding = maxRadius + stroke / 2;
  const offsetX = (WIDTH - base) / 2;
  const offsetY = (HEIGHT - base) / 2;
  const scale = (v) => padding + v * (base - 2 * padding);
  const color = (position) => hslHex(data.hue - 45 + position * 90, 0.5, 0.55);

  const byId = new Map(data.nodes.map((n) => [n.id, n]));
  const shapes = data.edges.map((e) => {
    const s = byId.get(e.source);
    const t = byId.get(e.target);
    return `<line x1="${num(scale(s.x) + offsetX)}" y1="${num(scale(s.y) + offsetY)}" x2="${num(scale(t.x) + offsetX)}" y2="${num(scale(t.y) + offsetY)}" stroke="${EDGE}" stroke-width="${num(stroke)}"/>`;
  });
  for (const n of [...data.nodes].sort((a, b) => a.z - b.z)) {
    shapes.push(
      `<circle cx="${num(scale(n.x) + offsetX)}" cy="${num(scale(n.y) + offsetY)}" r="${num(minRadius + n.z * (maxRadius - minRadius))}" fill="${color(n.position)}" stroke="${LIGHT}" stroke-width="${num(stroke)}"/>`
    );
  }
  return shapes.join('');
}

/** Compose the card's SVG: scatter background, radial blur, wordmark. */
export function cardSvg({ embeddingsKey } = {}) {
  const background = `<rect width="${WIDTH}" height="${HEIGHT}" fill="${LIGHT}"/>`;
  const data = embeddings[embeddingsKey];
  const scatter =
    data && data.nodes.length > 0
      ? SOFTEN_DEFS +
        `<g>${scatterShapes(data)}</g>` +
        `<g filter="url(#og-soften)" mask="url(#og-fade-mask)">${scatterShapes(data)}</g>`
      : '';
  return (
    `<svg width="${WIDTH}" height="${HEIGHT}" viewBox="0 0 ${WIDTH} ${HEIGHT}" xmlns="http://www.w3.org/2000/svg">` +
    background +
    scatter +
    `<g transform="translate(72 52) scale(2)">${WORDMARK}</g>` +
    `</svg>`  );
}

/** Render a social card to a PNG Response. */
export function cardResponse(options = {}) {
  const png = new Resvg(cardSvg(options)).render().asPng();
  return new Response(png, { headers: { 'Content-Type': 'image/png' } });
}

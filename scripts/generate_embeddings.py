#!/usr/bin/env python3
# /// script
# requires-python = "~=3.12.0"
# dependencies = ["numpy<2.5", "nltk", "sentence-transformers", "umap-learn"]
# ///
"""
Embedding pipeline for page visualization.

Generates 3D coordinates + similarity edges from page content using
sentence-transformers and UMAP. This is a standalone reimplementation of the
original Wagtail pipeline: instead of rendering a Wagtail template block, it
scans a directory of built ``index.html`` files and extracts text directly.

Pinned to Python 3.12 to match the environment that produced the original
embeddings. ``numpy<2.5`` is required so the resolver selects a modern ``numba``
with prebuilt wheels: with unconstrained numpy it pins numba 0.53.1 (whose
``llvmlite`` only supports Python <3.10 and has no installable wheel).

Run::

    uv run scripts/generate_embeddings.py --output static/embeddings.json
"""

import argparse
import hashlib
import json
import sys
from html.parser import HTMLParser
from pathlib import Path

import nltk
import numpy as np
from sentence_transformers import SentenceTransformer
from umap import UMAP

# Download punkt_tab tokenizer if needed
try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab", quiet=True)

# Block-level HTML elements. The original pipeline derived this set from
# markdown.Markdown().block_level_elements; the standard list is hardcoded here
# so the script has no dependency on the markdown library.
BLOCK_TAGS = {
    "address",
    "article",
    "aside",
    "blockquote",
    "details",
    "div",
    "dl",
    "dd",
    "fieldset",
    "figcaption",
    "figure",
    "footer",
    "form",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "header",
    "hgroup",
    "hr",
    "li",
    "main",
    "nav",
    "ol",
    "p",
    "pre",
    "section",
    "summary",
    "table",
    "ul",
}

# Elements to skip entirely (non-content)
SKIP_TAGS = {"script", "style", "nav", "header", "footer", "aside", "head", "meta"}

# Minimum sentence length (characters) to keep
MIN_SENTENCE_LENGTH = 10

# Cosine similarity threshold for creating an edge
SIMILARITY_THRESHOLD = 0.5

# sentence-transformers model name
MODEL_NAME = "all-MiniLM-L6-v2"

# The model is expensive to load; cache it across calls.
_MODEL = None


class HTMLTextExtractor(HTMLParser):
    """Extract text from HTML, respecting block structure."""

    def __init__(self):
        super().__init__()
        self.chunks = []
        self.current_text = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in SKIP_TAGS:
            self.skip_depth += 1
        elif tag in BLOCK_TAGS and self.current_text:
            self._flush_text()

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS:
            self.skip_depth -= 1
        elif tag in BLOCK_TAGS:
            self._flush_text()

    def handle_data(self, data):
        if self.skip_depth == 0:
            self.current_text.append(data)

    def _flush_text(self):
        if self.current_text:
            text = "".join(self.current_text).strip()
            if text:
                self.chunks.append(text)
            self.current_text = []

    def get_chunks(self):
        self._flush_text()
        return self.chunks


def chunk_html_to_sentences(html: str) -> list[str]:
    """
    Extract sentences from HTML content.

    Parses HTML structure, extracts text from block elements, and splits into
    sentences using NLTK.

    Args:
        html: HTML string

    Returns:
        List of sentences with a minimum length of ``MIN_SENTENCE_LENGTH``.
    """
    extractor = HTMLTextExtractor()
    extractor.feed(html)
    chunks = extractor.get_chunks()

    sentences = []
    for chunk in chunks:
        sentences.extend(nltk.sent_tokenize(chunk))

    return [s.strip() for s in sentences if len(s.strip()) >= MIN_SENTENCE_LENGTH]


def generate_embeddings(
    sentences: list[str], model_name: str = MODEL_NAME
) -> np.ndarray:
    """
    Generate embeddings for a list of sentences using sentence-transformers.

    Args:
        sentences: List of sentence strings
        model_name: Name of the sentence-transformers model to use

    Returns:
        NumPy array of shape (n_sentences, embedding_dim)
    """
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer(model_name)
    embeddings = _MODEL.encode(sentences, show_progress_bar=False)
    return embeddings


def reduce_to_3d(
    embeddings: np.ndarray, n_neighbors: int = 15, min_dist: float = 0.1
) -> np.ndarray:
    """
    Reduce high-dimensional embeddings to 3D using UMAP.

    Args:
        embeddings: NumPy array of shape (n_sentences, embedding_dim)
        n_neighbors: UMAP n_neighbors parameter (local vs global structure)
        min_dist: UMAP min_dist parameter (clustering tightness)

    Returns:
        NumPy array of shape (n_sentences, 3) with normalized 0-1 coordinates
    """
    n_samples = embeddings.shape[0]

    # UMAP needs at least 2 samples
    if n_samples < 2:
        # Return center point for single sample
        return np.array([[0.5, 0.5, 0.5]])

    # Adjust n_neighbors for small datasets
    adjusted_neighbors = min(n_neighbors, n_samples - 1)

    reducer = UMAP(
        n_components=3,
        n_neighbors=adjusted_neighbors,
        min_dist=min_dist,
        metric="cosine",
        random_state=42,
        n_jobs=1,
    )

    coords_3d = reducer.fit_transform(embeddings)

    # Normalize each dimension to 0-1 range
    min_vals = coords_3d.min(axis=0)
    max_vals = coords_3d.max(axis=0)
    range_vals = max_vals - min_vals

    # Avoid division by zero
    range_vals[range_vals == 0] = 1

    normalized = (coords_3d - min_vals) / range_vals

    return normalized


def compute_cosine_similarities(
    embeddings: np.ndarray, threshold: float = SIMILARITY_THRESHOLD
) -> list[tuple[int, int, float]]:
    """
    Compute pairwise cosine similarities between embeddings.

    Args:
        embeddings: NumPy array of shape (n_sentences, embedding_dim)
        threshold: Minimum similarity to include (0-1)

    Returns:
        List of (source_id, target_id, similarity) tuples for pairs above threshold
    """
    # Normalize embeddings for cosine similarity
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1  # Avoid division by zero
    normalized = embeddings / norms

    # Compute cosine similarity matrix
    similarity_matrix = np.dot(normalized, normalized.T)

    edges = []
    n = len(embeddings)
    for i in range(n):
        for j in range(i + 1, n):
            sim = similarity_matrix[i, j]
            if sim >= threshold:
                edges.append((i, j, float(sim)))

    return edges


def compute_content_hue(embeddings: np.ndarray) -> float:
    """
    Derive a unique hue (0-360) from article embeddings.

    Uses a hash of the mean embedding to get a well-distributed position on the
    color spectrum for each article.

    Args:
        embeddings: NumPy array of shape (n_sentences, embedding_dim)

    Returns:
        Hue value between 0 and 360
    """
    # Compute mean embedding for the article
    mean_embedding = embeddings.mean(axis=0)

    # Hash the embedding to get a well-distributed value
    emb_bytes = mean_embedding.tobytes()
    hash_digest = hashlib.sha256(emb_bytes).hexdigest()

    # Use first 8 hex chars (32 bits) to derive hue
    hash_int = int(hash_digest[:8], 16)
    hue = hash_int % 360

    return float(hue)


def generate_visualization_data(
    html: str, similarity_threshold: float = SIMILARITY_THRESHOLD
) -> dict:
    """
    Generate complete visualization data from page HTML.

    Args:
        html: The rendered page HTML
        similarity_threshold: Minimum cosine similarity for edge creation (0-1)

    Returns:
        Dict with:
        - nodes: array with id, x, y, z (for size), text, position
        - edges: array with source, target, similarity
        - hue: content-derived hue (0-360) for color gradient
    """
    sentences = chunk_html_to_sentences(html)

    if not sentences:
        return {"nodes": [], "edges": [], "hue": 0}

    embeddings = generate_embeddings(sentences)
    coords = reduce_to_3d(embeddings)
    edge_tuples = compute_cosine_similarities(
        embeddings, threshold=similarity_threshold
    )
    hue = compute_content_hue(embeddings)

    nodes = []
    for i, (sentence, (x, y, z)) in enumerate(zip(sentences, coords)):
        position = i / max(len(sentences) - 1, 1)
        nodes.append(
            {
                "id": i,
                "x": float(x),
                "y": float(y),
                "z": float(z),
                "text": sentence,
                "position": float(position),
            }
        )

    edges = [
        {"source": src, "target": tgt, "similarity": sim}
        for src, tgt, sim in edge_tuples
    ]

    return {"nodes": nodes, "edges": edges, "hue": hue}


def derive_key(rel_path: Path) -> str | None:
    """
    Derive a visualization key from a file path relative to the input directory.

    ``index.html``          -> ``home``
    ``articles/index.html`` -> ``articles`` (harmless if unused)
    ``articles/<slug>/index.html`` -> ``articles/<slug>``

    Returns ``None`` for files that should be skipped (e.g. ``404.html``).
    """
    rel_posix = rel_path.as_posix()

    # Defensive: skip the error page explicitly (also naturally excluded because
    # we only glob for index.html files).
    if rel_posix == "404.html":
        return None

    if rel_posix == "index.html":
        return "home"

    if not rel_posix.endswith("/index.html"):
        return None

    # Strip the trailing "/index.html"
    return rel_posix[: -len("/index.html")]


def discover_pages(input_dir: Path) -> list[tuple[str, Path]]:
    """Find index.html files under ``input_dir`` and derive their keys."""
    pages = []
    for index_path in sorted(input_dir.rglob("index.html")):
        rel = index_path.relative_to(input_dir)
        key = derive_key(rel)
        if key is not None:
            pages.append((key, index_path))
    return pages


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate embedding visualization data from built HTML."
    )
    parser.add_argument(
        "--input",
        default="build",
        help="Directory to scan for index.html files (default: build)",
    )
    parser.add_argument(
        "--output",
        default="static/embeddings.json",
        help="Output JSON path (default: static/embeddings.json)",
    )
    args = parser.parse_args(argv)

    input_dir = Path(args.input)
    output_path = Path(args.output)

    if not input_dir.is_dir():
        print(f"Input directory not found: {input_dir}", file=sys.stderr)
        return 1

    pages = discover_pages(input_dir)
    if not pages:
        print(f"No index.html files found under {input_dir}", file=sys.stderr)
        return 1

    print(f"Found {len(pages)} page(s) under {input_dir}:", file=sys.stderr)
    for key, path in pages:
        print(f"  {key} -> {path.relative_to(input_dir)}", file=sys.stderr)

    result = {}
    for key, index_path in pages:
        html = index_path.read_text(encoding="utf-8")
        data = generate_visualization_data(html)
        result[key] = data
        print(
            f"{key}: {len(data['nodes'])} nodes, {len(data['edges'])} edges, "
            f"hue {data['hue']}",
            file=sys.stderr,
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Wrote {output_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""
Embedding pipeline for page visualization.

Generates 2D coordinates from page content using sentence-transformers and UMAP.
Works with any Wagtail page by extracting text from rendered HTML.
"""

import logging
from html.parser import HTMLParser

import markdown
import nltk
import numpy as np
from sentence_transformers import SentenceTransformer
from umap import UMAP

logger = logging.getLogger(__name__)

# Download punkt_tab tokenizer if needed
try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab", quiet=True)

# Block-level HTML elements from markdown library
BLOCK_TAGS = set(markdown.Markdown().block_level_elements)

# Elements to skip entirely (non-content)
SKIP_TAGS = {"script", "style", "nav", "header", "footer", "aside", "head", "meta"}


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

    Parses HTML structure, extracts text from block elements,
    and splits into sentences using NLTK.

    Args:
        html: HTML string

    Returns:
        List of sentences with minimum length of 10 characters
    """
    extractor = HTMLTextExtractor()
    extractor.feed(html)
    chunks = extractor.get_chunks()

    sentences = []
    for chunk in chunks:
        sentences.extend(nltk.sent_tokenize(chunk))

    return [s.strip() for s in sentences if len(s.strip()) >= 10]


def generate_embeddings(
    sentences: list[str], model_name: str = "all-MiniLM-L6-v2"
) -> np.ndarray:
    """
    Generate embeddings for a list of sentences using sentence-transformers.

    Args:
        sentences: List of sentence strings
        model_name: Name of the sentence-transformers model to use

    Returns:
        NumPy array of shape (n_sentences, embedding_dim)
    """
    model = SentenceTransformer(model_name)
    embeddings = model.encode(sentences, show_progress_bar=False)
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
    embeddings: np.ndarray, threshold: float = 0.5
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


def generate_visualization_data(html: str, similarity_threshold: float = 0.5) -> dict:
    """
    Generate complete visualization data from page HTML.

    Args:
        html: The rendered page HTML
        similarity_threshold: Minimum cosine similarity for edge creation (0-1)

    Returns:
        Dict with:
        - nodes: array with id, x, y, z (for size), text, position
        - edges: array with source, target, similarity
    """
    sentences = chunk_html_to_sentences(html)

    if not sentences:
        return {"nodes": [], "edges": []}

    embeddings = generate_embeddings(sentences)
    coords = reduce_to_3d(embeddings)
    edge_tuples = compute_cosine_similarities(
        embeddings, threshold=similarity_threshold
    )

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

    return {"nodes": nodes, "edges": edges}


def render_page_to_html(page, block_name: str = "content") -> str:
    """
    Render a specific block from a Wagtail page's template.

    Args:
        page: A Wagtail Page instance
        block_name: Name of the template block to render

    Returns:
        Rendered HTML string of the specified block
    """
    from django.template import RequestContext
    from django.template.loader import get_template
    from django.template.loader_tags import (
        BlockContext,
        BlockNode,
        ExtendsNode,
        BLOCK_CONTEXT_KEY,
    )
    from django.test import RequestFactory

    request = RequestFactory().get(page.url or "/")
    template = get_template(page.template).template
    context = RequestContext(request, page.get_context(request))

    # Collect all blocks from the template hierarchy
    blocks = {}

    def collect_blocks(nodelist):
        for node in nodelist:
            if isinstance(node, BlockNode):
                blocks[node.name] = node
            if isinstance(node, ExtendsNode):
                # Collect blocks defined in this child template
                blocks.update(node.blocks)

    collect_blocks(template.nodelist)

    # Set up block context and render the requested block
    block_context = BlockContext()
    block_context.add_blocks(blocks)

    with context.render_context.push_state(template):
        context.render_context[BLOCK_CONTEXT_KEY] = block_context
        block = block_context.get_block(block_name)
        return block.nodelist.render(context)

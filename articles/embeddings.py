"""
Embedding pipeline for article visualization.

Generates 2D coordinates from article text using sentence-transformers and UMAP.
"""

import json
import logging
import re

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


def chunk_to_sentences(text: str) -> list[str]:
    """
    Split text into sentences using NLTK.

    Strips markdown syntax and returns clean sentences.
    """
    # Remove markdown links but keep text: [text](url) -> text
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)

    # Remove markdown images: ![alt](url)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)

    # Remove inline code: `code`
    text = re.sub(r"`[^`]+`", "", text)

    # Remove code blocks: ```...```
    text = re.sub(r"```[\s\S]*?```", "", text)

    # Remove headers: # Header
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)

    # Remove bold/italic markers
    text = re.sub(r"\*{1,2}([^*]+)\*{1,2}", r"\1", text)
    text = re.sub(r"_{1,2}([^_]+)_{1,2}", r"\1", text)

    # Remove blockquotes
    text = re.sub(r"^>\s+", "", text, flags=re.MULTILINE)

    # Remove list markers
    text = re.sub(r"^[\-\*\+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\d+\.\s+", "", text, flags=re.MULTILINE)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    sentences = nltk.sent_tokenize(text)

    # Filter out very short sentences (< 10 chars)
    sentences = [s.strip() for s in sentences if len(s.strip()) >= 10]

    return sentences


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
        random_state=42,  # Reproducible results
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


def generate_visualization_data(text: str, similarity_threshold: float = 0.5) -> dict:
    """
    Generate complete visualization data from article text.

    Args:
        text: The article body text (markdown)
        similarity_threshold: Minimum cosine similarity for edge creation (0-1)

    Returns:
        Dict with:
        - nodes: array with id, x, y, z (for size), text, position
        - edges: array with source, target, similarity
    """
    sentences = chunk_to_sentences(text)

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
                "text": sentence[:100] + "..." if len(sentence) > 100 else sentence,
                "position": float(position),
            }
        )

    edges = [
        {"source": src, "target": tgt, "similarity": sim}
        for src, tgt, sim in edge_tuples
    ]

    return {"nodes": nodes, "edges": edges}


def visualization_data_to_json(data: dict) -> str:
    """Serialize visualization data to JSON string."""
    return json.dumps(data)

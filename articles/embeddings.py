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


def reduce_to_2d(
    embeddings: np.ndarray, n_neighbors: int = 15, min_dist: float = 0.1
) -> np.ndarray:
    """
    Reduce high-dimensional embeddings to 2D using UMAP.

    Args:
        embeddings: NumPy array of shape (n_sentences, embedding_dim)
        n_neighbors: UMAP n_neighbors parameter (local vs global structure)
        min_dist: UMAP min_dist parameter (clustering tightness)

    Returns:
        NumPy array of shape (n_sentences, 2) with normalized 0-1 coordinates
    """
    n_samples = embeddings.shape[0]

    # UMAP needs at least 2 samples
    if n_samples < 2:
        # Return center point for single sample
        return np.array([[0.5, 0.5]])

    # Adjust n_neighbors for small datasets
    adjusted_neighbors = min(n_neighbors, n_samples - 1)

    reducer = UMAP(
        n_components=2,
        n_neighbors=adjusted_neighbors,
        min_dist=min_dist,
        metric="cosine",
        random_state=42,  # Reproducible results
    )

    coords_2d = reducer.fit_transform(embeddings)

    # Normalize to 0-1 range
    min_vals = coords_2d.min(axis=0)
    max_vals = coords_2d.max(axis=0)
    range_vals = max_vals - min_vals

    # Avoid division by zero
    range_vals[range_vals == 0] = 1

    normalized = (coords_2d - min_vals) / range_vals

    return normalized


def generate_visualization_data(text: str) -> dict:
    """
    Generate complete visualization data from article text.

    Args:
        text: The article body text (markdown)

    Returns:
        Dict with nodes array containing id, x, y, text, and position for each sentence
    """
    sentences = chunk_to_sentences(text)

    if not sentences:
        return {"nodes": []}

    embeddings = generate_embeddings(sentences)
    coords = reduce_to_2d(embeddings)

    nodes = []
    for i, (sentence, (x, y)) in enumerate(zip(sentences, coords)):
        position = i / max(len(sentences) - 1, 1)
        nodes.append(
            {
                "id": i,
                "x": float(x),
                "y": float(y),
                "text": sentence[:100] + "..." if len(sentence) > 100 else sentence,
                "position": float(position),
            }
        )

    return {"nodes": nodes}


def visualization_data_to_json(data: dict) -> str:
    """Serialize visualization data to JSON string."""
    return json.dumps(data)

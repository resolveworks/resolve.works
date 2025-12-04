"""
Signal handlers for embedding generation.
"""

import logging

from wagtail.signals import page_published

logger = logging.getLogger(__name__)


def generate_page_embeddings(sender, **kwargs):
    """
    Generate embedding visualization when a page with EmbeddingMixin is published.
    """
    from embeddings.models import EmbeddingMixin

    instance = kwargs.get("instance")

    if not isinstance(instance, EmbeddingMixin):
        return

    logger.info(f"Generating embeddings for page: {instance.title}")

    instance.generate_embedding_visualization()

    # Save without triggering another publish signal
    type(instance).objects.filter(pk=instance.pk).update(
        embedding_visualization=instance.embedding_visualization
    )


def register_signal_handlers():
    """Register signal handlers for embedding generation."""
    page_published.connect(generate_page_embeddings)

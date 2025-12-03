"""
Signal handlers for article embedding generation.
"""

import logging

from wagtail.signals import page_published

logger = logging.getLogger(__name__)


def generate_article_embeddings(sender, **kwargs):
    """
    Generate embedding visualization when an ArticlePage is published.
    """
    from articles.models import ArticlePage

    instance = kwargs.get("instance")

    if not isinstance(instance, ArticlePage):
        return

    logger.info(f"Generating embeddings for article: {instance.title}")

    instance.generate_embedding_visualization()

    # Save without triggering another publish signal
    ArticlePage.objects.filter(pk=instance.pk).update(
        embedding_visualization=instance.embedding_visualization
    )


def register_signal_handlers():
    """Register signal handlers for the articles app."""
    page_published.connect(generate_article_embeddings)

"""
Reusable model mixins for embedding visualization.
"""

import logging

from django.db import models

logger = logging.getLogger(__name__)


class EmbeddingMixin(models.Model):
    """
    Mixin that adds embedding visualization support to any Wagtail Page.

    Stores pre-computed 2D/3D coordinates for visualizing page content
    as a semantic graph.
    """

    embedding_visualization = models.JSONField(
        blank=True,
        null=True,
        editable=False,
        help_text="Pre-computed coordinates for embedding visualization",
    )

    class Meta:
        abstract = True

    def generate_embedding_visualization(self):
        """Generate and store embedding visualization data for this page."""
        from embeddings.embeddings import (
            generate_visualization_data,
            render_page_to_html,
        )

        try:
            html = render_page_to_html(self)
            self.embedding_visualization = generate_visualization_data(html)
            logger.info(
                f"Generated embedding visualization for '{self.title}' "
                f"with {len(self.embedding_visualization.get('nodes', []))} nodes"
            )
        except Exception as e:
            logger.exception(f"Failed to generate embedding visualization: {e}")
            self.embedding_visualization = {"nodes": [], "edges": []}

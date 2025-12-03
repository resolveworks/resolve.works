import logging

from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtailmarkdown.fields import MarkdownField

from home.models import SeoMixin

logger = logging.getLogger(__name__)


class ArticleIndexPage(Page):
    """Index page that lists all articles."""

    intro = RichTextField(blank=True, features=["bold", "italic", "link"])

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    subpage_types = ["articles.ArticlePage"]
    parent_page_types = ["home.HomePage"]

    def get_context(self, request):
        context = super().get_context(request)
        context["articles"] = (
            ArticlePage.objects.live()
            .descendant_of(self)
            .order_by("-first_published_at")
        )
        return context

    class Meta:
        verbose_name = "Article Index"


class ArticlePage(SeoMixin, Page):
    """Individual article page."""

    intro = models.CharField(
        max_length=500,
        blank=True,
        help_text="Brief introduction shown in article listings",
    )

    body = MarkdownField()

    embedding_visualization = models.JSONField(
        blank=True,
        null=True,
        editable=False,
        help_text="Pre-computed 2D coordinates for embedding visualization",
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

    promote_panels = Page.promote_panels + SeoMixin.seo_panels

    parent_page_types = ["articles.ArticleIndexPage"]
    subpage_types = []

    @property
    def og_type(self):
        return "article"

    def generate_embedding_visualization(self):
        """Generate and store embedding visualization data for this article."""
        from articles.embeddings import generate_visualization_data

        if not self.body:
            self.embedding_visualization = {"nodes": []}
            return

        try:
            self.embedding_visualization = generate_visualization_data(self.body)
            logger.info(
                f"Generated embedding visualization for '{self.title}' "
                f"with {len(self.embedding_visualization.get('nodes', []))} nodes"
            )
        except Exception as e:
            logger.exception(f"Failed to generate embedding visualization: {e}")
            self.embedding_visualization = {"nodes": []}

    class Meta:
        verbose_name = "Article"

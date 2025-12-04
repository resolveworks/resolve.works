from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtailmarkdown.fields import MarkdownField

from home.models import SeoMixin
from embeddings.models import EmbeddingMixin


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


class ArticlePage(EmbeddingMixin, SeoMixin, Page):
    """Individual article page."""

    intro = models.CharField(
        max_length=500,
        blank=True,
        help_text="Brief introduction shown in article listings",
    )

    body = MarkdownField()

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

    class Meta:
        verbose_name = "Article"

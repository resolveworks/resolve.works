from django.conf import settings
from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail import blocks

from .blocks import HeroBlock, SectionBlock, DefinitionListBlock, ProcessRoadmapBlock


class SeoMixin(models.Model):
    """Mixin for SEO fields shared across page types."""

    og_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Image for social media sharing (recommended: 1200x630px)",
    )

    robots = models.CharField(
        max_length=100,
        default="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1",
        help_text="Robots meta tag value",
    )

    seo_panels = [
        MultiFieldPanel(
            [
                FieldPanel("og_image"),
                FieldPanel("robots"),
            ],
            heading="SEO Settings",
        ),
    ]

    @property
    def og_type(self):
        """Override in subclasses for different page types."""
        return "website"

    class Meta:
        abstract = True


@register_setting
class BusinessSettings(BaseSiteSetting):
    """Business information for structured data and site-wide use."""

    name = models.CharField(max_length=100, default="Resolve")
    description = models.TextField(blank=True)
    telephone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    address_country = models.CharField(max_length=100, blank=True, default="Netherlands")
    price_range = models.CharField(max_length=10, blank=True, default="€€€")
    opening_hours = models.CharField(max_length=100, blank=True, default="Mo-Fr 09:00-18:00")
    founder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        FieldPanel("telephone"),
        FieldPanel("email"),
        FieldPanel("address_country"),
        FieldPanel("price_range"),
        FieldPanel("opening_hours"),
        FieldPanel("founder"),
    ]

    class Meta:
        verbose_name = "Business Information"


@register_setting
class FooterSettings(BaseSiteSetting):
    """Global footer settings."""

    heading = models.CharField(
        max_length=100, default="Resolve", help_text="Footer heading"
    )

    column_1 = StreamField(
        [
            ("paragraph", blocks.RichTextBlock(features=["bold", "italic", "link"])),
            ("definition_list", DefinitionListBlock()),
        ],
        blank=True,
        use_json_field=True,
        help_text="First footer column content",
    )

    column_2 = StreamField(
        [
            ("paragraph", blocks.RichTextBlock(features=["bold", "italic", "link"])),
            ("definition_list", DefinitionListBlock()),
        ],
        blank=True,
        use_json_field=True,
        help_text="Second footer column content",
    )

    column_3 = StreamField(
        [
            ("paragraph", blocks.RichTextBlock(features=["bold", "italic", "link"])),
            ("definition_list", DefinitionListBlock()),
        ],
        blank=True,
        use_json_field=True,
        help_text="Third footer column content",
    )

    panels = [
        FieldPanel("heading"),
        MultiFieldPanel(
            [
                FieldPanel("column_1"),
                FieldPanel("column_2"),
                FieldPanel("column_3"),
            ],
            heading="Footer Columns",
        ),
    ]

    class Meta:
        verbose_name = "Footer"


class HomePage(SeoMixin, Page):
    body = StreamField(
        [("hero", HeroBlock()), ("section", SectionBlock())],
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    promote_panels = Page.promote_panels + SeoMixin.seo_panels

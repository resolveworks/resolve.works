from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail import blocks

from .blocks import HeroBlock, SectionBlock, DefinitionListBlock, ProcessRoadmapBlock


@register_setting
class FooterSettings(BaseSiteSetting):
    """Global footer settings."""

    heading = models.CharField(
        max_length=100,
        default="Resolve",
        help_text="Footer heading"
    )

    column_1 = StreamField(
        [
            ("paragraph", blocks.RichTextBlock(features=["bold", "italic", "link"])),
            ("definition_list", DefinitionListBlock()),
        ],
        blank=True,
        use_json_field=True,
        help_text="First footer column content"
    )

    column_2 = StreamField(
        [
            ("paragraph", blocks.RichTextBlock(features=["bold", "italic", "link"])),
            ("definition_list", DefinitionListBlock()),
        ],
        blank=True,
        use_json_field=True,
        help_text="Second footer column content"
    )

    column_3 = StreamField(
        [
            ("paragraph", blocks.RichTextBlock(features=["bold", "italic", "link"])),
            ("definition_list", DefinitionListBlock()),
        ],
        blank=True,
        use_json_field=True,
        help_text="Third footer column content"
    )

    panels = [
        FieldPanel("heading"),
        MultiFieldPanel(
            [
                FieldPanel("column_1"),
                FieldPanel("column_2"),
                FieldPanel("column_3"),
            ],
            heading="Footer Columns"
        ),
    ]

    class Meta:
        verbose_name = "Footer"


class HomePage(Page):
    body = StreamField(
        [
            ("hero", HeroBlock()),
            ("section", SectionBlock()),
            ("process_roadmap", ProcessRoadmapBlock()),
        ],
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

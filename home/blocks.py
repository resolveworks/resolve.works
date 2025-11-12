"""Shared blocks for the Resolve.works site."""

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class HeroBlock(blocks.StructBlock):
    """Hero block for homepage header."""

    heading = blocks.CharBlock(
        required=True, max_length=255, help_text="Main heading text"
    )

    body_text = blocks.TextBlock(
        required=True, help_text="Body text for the hero section"
    )

    cta_email = blocks.EmailBlock(required=False, help_text="Email address for contact")

    cta_phone = blocks.CharBlock(
        required=False, max_length=50, help_text="Phone number for contact"
    )

    class Meta:
        icon = "placeholder"
        label = "Hero Section"
        template = "blocks/hero_block.html"


class FeatureItemBlock(blocks.StructBlock):
    """Individual feature item."""

    heading = blocks.CharBlock(required=True, max_length=100)
    description = blocks.RichTextBlock(features=["bold", "italic", "link"])

    class Meta:
        icon = "list-ul"


class FeaturesBlock(blocks.StructBlock):
    """Configurable features list with 3 or 4 columns."""

    columns = blocks.ChoiceBlock(
        choices=[
            ("3", "3 columns (h4 headings)"),
            ("4", "4 columns (h6 headings)"),
        ],
        default="3",
        help_text="Number of columns in grid layout",
    )
    features = blocks.ListBlock(FeatureItemBlock())

    class Meta:
        icon = "list-ul"
        label = "Features"
        template = "blocks/features_block.html"


class DefinitionListItemBlock(blocks.StructBlock):
    """Individual term-definition pair for a definition list."""

    term = blocks.CharBlock(required=True, max_length=100, help_text="Definition term (dt)")
    definition = blocks.RichTextBlock(
        required=True,
        features=["bold", "italic", "link"],
        help_text="Definition description (dd)"
    )

    class Meta:
        icon = "list-ul"


class DefinitionListBlock(blocks.StructBlock):
    """Definition list (dl) with term-definition pairs."""

    items = blocks.ListBlock(DefinitionListItemBlock())

    class Meta:
        icon = "list-ul"
        label = "Definition List"
        template = "blocks/definition_list_block.html"


class TwoColumnBlock(blocks.StructBlock):
    """Two-column layout with image on one side and content on the other."""

    image_position = blocks.ChoiceBlock(
        choices=[
            ("left", "Image on left"),
            ("right", "Image on right"),
        ],
        default="right",
        help_text="Which side to place the image",
    )

    image = ImageChooserBlock(required=True, help_text="Image for the column")

    content = blocks.StreamBlock(
        [
            (
                "heading",
                blocks.RichTextBlock(
                    features=["h4"], help_text="Heading (h4)"
                ),
            ),
            (
                "paragraph",
                blocks.RichTextBlock(
                    features=["bold", "italic", "link"], help_text="Paragraph of text"
                ),
            ),
            ("definition_list", DefinitionListBlock()),
        ],
        required=True,
        help_text="Content for the text column",
    )

    class Meta:
        icon = "image"
        label = "Two Column (Image + Content)"
        template = "blocks/two_column_block.html"


class FAQItemBlock(blocks.StructBlock):
    """Individual FAQ question and answer."""

    question = blocks.CharBlock(
        required=True,
        max_length=255,
        help_text="The question"
    )
    answer = blocks.RichTextBlock(
        required=True,
        features=["bold", "italic", "link"],
        help_text="The answer"
    )

    class Meta:
        icon = "help"


class FAQBlock(blocks.StructBlock):
    """FAQ section with structured data support."""

    items = blocks.ListBlock(FAQItemBlock(), help_text="FAQ items")

    def get_structured_data(self):
        """Generate JSON-LD structured data for this FAQ block."""
        if not self.get('items'):
            return None

        return {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": item['question'],
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": item['answer'].source  # Get the raw HTML
                    }
                }
                for item in self.get('items', [])
            ]
        }

    class Meta:
        icon = "help"
        label = "FAQ"
        template = "blocks/faq_block.html"


class ProcessStepBlock(blocks.StructBlock):
    """Individual step in the process roadmap."""

    title = blocks.CharBlock(
        required=True,
        max_length=100,
        help_text="Step title (e.g., 'Diagnose', 'Prototype')"
    )
    description = blocks.TextBlock(
        required=True,
        help_text="Brief description of this step"
    )

    class Meta:
        icon = "list-ol"


class ProcessRoadmapBlock(blocks.StructBlock):
    """From Roadmap to Rollout section with animated arrows."""

    heading = blocks.CharBlock(
        required=True,
        default="From roadmap to rollout",
        max_length=255,
        help_text="Section heading"
    )
    steps = blocks.ListBlock(
        ProcessStepBlock(),
        min_num=4,
        max_num=4,
        help_text="Exactly 4 process steps (arrows connect first 3)"
    )

    class Meta:
        icon = "doc-full"
        label = "Process Roadmap"
        template = "blocks/process_roadmap.html"


class SectionBlock(blocks.StructBlock):
    """Generic section block with title, background, and flexible content."""

    title = blocks.CharBlock(
        required=True, max_length=255, help_text="Section title (h2)"
    )

    background = blocks.ChoiceBlock(
        choices=[
            ("light", "Light"),
            ("dark", "Dark"),
        ],
        default="light",
        help_text="Section background color",
    )

    content = blocks.StreamBlock(
        [
            (
                "heading",
                blocks.RichTextBlock(
                    features=["h4"], help_text="Heading (h4)"
                ),
            ),
            (
                "paragraph",
                blocks.RichTextBlock(
                    features=["bold", "italic", "link"], help_text="Paragraph of text"
                ),
            ),
            ("features", FeaturesBlock()),
            ("definition_list", DefinitionListBlock()),
            ("two_column", TwoColumnBlock()),
            ("faq", FAQBlock()),
        ],
        required=False,
    )

    class Meta:
        icon = "doc-full"
        label = "Section"
        template = "blocks/section_block.html"

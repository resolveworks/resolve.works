from django.conf import settings
from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

from resolve.fields import PhoneField
from embeddings.models import EmbeddingMixin

from .blocks import HeroBlock, SectionBlock


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
    phone = PhoneField()
    email = models.EmailField(blank=True)
    address_country = models.CharField(
        max_length=100, blank=True, default="Netherlands"
    )
    price_range = models.CharField(max_length=10, blank=True, default="€€€")
    opening_hours = models.CharField(
        max_length=100, blank=True, default="Mo-Fr 09:00-18:00"
    )
    founder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    # Social links
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn profile URL")
    github_url = models.URLField(blank=True, help_text="GitHub profile URL")

    # Business registration
    address = models.TextField(blank=True, help_text="Full business address")
    vat_number = models.CharField(
        max_length=50, blank=True, help_text="VAT registration number"
    )
    register_url = models.URLField(blank=True, help_text="Business register URL")

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("description"),
                FieldPanel("founder"),
            ],
            heading="Basic Information",
        ),
        MultiFieldPanel(
            [
                FieldPanel("phone"),
                FieldPanel("email"),
                FieldPanel("linkedin_url"),
                FieldPanel("github_url"),
            ],
            heading="Contact",
        ),
        MultiFieldPanel(
            [
                FieldPanel("address"),
                FieldPanel("address_country"),
                FieldPanel("vat_number"),
                FieldPanel("register_url"),
            ],
            heading="Business Registration",
        ),
        MultiFieldPanel(
            [
                FieldPanel("price_range"),
                FieldPanel("opening_hours"),
            ],
            heading="Structured Data",
        ),
    ]

    class Meta:
        verbose_name = "Business"


@register_setting
class ContactSettings(BaseSiteSetting):
    """Contact email template settings."""

    email_subject = models.CharField(
        max_length=200,
        default="Free consultation request",
        help_text="Subject line for contact emails",
    )
    email_body = models.TextField(
        default="Hi,\n\nWe're curious about how you could help us with our current challenge.\n\n...\n\nBest regards,\n...",
        help_text="Default email body template",
    )

    panels = [
        FieldPanel("email_subject"),
        FieldPanel("email_body"),
    ]

    class Meta:
        verbose_name = "Contact"


@register_setting
class FooterSettings(BaseSiteSetting):
    """Global footer settings."""

    heading = models.CharField(
        max_length=100, default="Resolve", help_text="Footer heading"
    )

    tagline = RichTextField(
        features=["bold", "italic", "link"],
        blank=True,
        help_text="Footer tagline content",
    )

    registration_note = models.CharField(
        max_length=200,
        blank=True,
        help_text="Note displayed below business registration info (e.g. 'Estonian e-residency program')",
    )

    panels = [
        FieldPanel("heading"),
        FieldPanel("tagline"),
        FieldPanel("registration_note"),
    ]

    class Meta:
        verbose_name = "Footer"


class HomePage(EmbeddingMixin, SeoMixin, Page):
    body = StreamField(
        [("hero", HeroBlock()), ("section", SectionBlock())],
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    promote_panels = Page.promote_panels + SeoMixin.seo_panels

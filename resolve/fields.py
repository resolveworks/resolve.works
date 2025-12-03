from django.core.validators import RegexValidator
from django.db import models


phone_validator = RegexValidator(
    regex=r"^\+\d+$",
    message="Phone number must start with + followed by digits only (e.g., +31612345678)",
)


class PhoneField(models.CharField):
    """CharField for phone numbers that validates + followed by digits."""

    default_validators = [phone_validator]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 20)
        kwargs.setdefault("blank", True)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs.get("max_length") == 20:
            del kwargs["max_length"]
        if kwargs.get("blank") is True:
            del kwargs["blank"]
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        """Add placeholder to form field."""
        defaults = {"help_text": "Format: +31612345678"}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def format_display(self):
        """Format for display with spaces in groups of three."""
        if not self:
            return ""
        # +31 612 345 678
        country_code = self[:3]
        rest = self[3:]
        groups = [rest[i : i + 3] for i in range(0, len(rest), 3)]
        return f"{country_code} {' '.join(groups)}"

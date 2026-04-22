from django import template

register = template.Library()


@register.filter
def format_phone(phone):
    """Format a phone number with spaces in groups of three.

    Expects a validated phone number in format +31612345678.
    Returns formatted display: +31 612 345 678.
    """
    if not phone:
        return ""
    phone = str(phone)
    groups = [phone[i : i + 3] for i in range(0, len(phone), 3)]
    return " ".join(groups)

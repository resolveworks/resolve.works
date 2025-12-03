from urllib.parse import urlparse

from django import template

register = template.Library()


@register.filter
def url_root(url):
    """Extract the root URL (scheme + netloc) from a full URL."""
    if not url:
        return ""
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"

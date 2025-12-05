from .base import (
    INSTALLED_APPS as BASE_INSTALLED_APPS,
    MIDDLEWARE as BASE_MIDDLEWARE,
)

# Development settings
DEBUG = True

# Add django-browser-reload for development
INSTALLED_APPS = BASE_INSTALLED_APPS + [
    "django_browser_reload",
]

MIDDLEWARE = BASE_MIDDLEWARE + [
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

# Allow all hosts in development
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

try:
    from .local import *  # noqa: F401, F403
except ImportError:
    pass

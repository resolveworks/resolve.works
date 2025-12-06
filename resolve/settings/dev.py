from .base import *  # noqa: F403

# Add django-browser-reload for development
INSTALLED_APPS = INSTALLED_APPS + [  # noqa: F405
    "django_browser_reload",
]

MIDDLEWARE = MIDDLEWARE + [  # noqa: F405
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

try:
    from .local import *  # noqa: F401, F403
except ImportError:
    pass

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Add django-browser-reload for development
INSTALLED_APPS = INSTALLED_APPS + [
    "django_browser_reload",
]

MIDDLEWARE = MIDDLEWARE + [
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-qtfk6mvo0m_-^uz=+u=_$(&%y-dwtccjz3a6(8fsdt-c#mjj6s"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

WAGTAILADMIN_BASE_URL = "http://localhost:8000"


try:
    from .local import *
except ImportError:
    pass

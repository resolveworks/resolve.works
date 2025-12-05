# Use an official Python runtime based on Debian 12 "bookworm" as a parent image.
FROM python:3.13-slim-bookworm

# Add user that will be used in the container.
RUN useradd --create-home wagtail

# Port used by this container to serve HTTP.
EXPOSE 8000

# PyTorch variant: "cpu" for smaller images, "cu128" for CUDA 12.8 support
ARG TORCH_EXTRA=cpu

# Set environment variables.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

# Install uv for dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock* ./

# Install dependencies with selected PyTorch variant
RUN uv sync --frozen --no-dev --no-install-project --extra $TORCH_EXTRA

# Copy the source code of the project into the container.
COPY --chown=wagtail:wagtail . .

# Set this directory to be owned by the "wagtail" user.
RUN chown -R wagtail:wagtail /app && mkdir -p /app/media && chown wagtail:wagtail /app/media

# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail

# Collect static files with production settings (for ManifestStaticFilesStorage).
RUN DJANGO_SETTINGS_MODULE=resolve.settings.production uv run --no-dev manage.py collectstatic --noinput --clear

# Runtime command that executes when "docker run" is called.
CMD ["uv", "run", "--no-dev", "gunicorn", "resolve.wsgi:application", "--bind", "0.0.0.0:8000"]

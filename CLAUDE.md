# Resolve.works

## Overview

Consulting site built with Wagtail CMS. Single-page homepage with section-based StreamField blocks, articles with AI-powered semantic search.

## Project Structure

- `resolve/` - Django project config (settings, urls, static files)
- `home/` - Homepage app with StreamField blocks
- `articles/` - Blog/articles with embedding-based visualization
- `accounts/` - Custom user model with work experience
- `images/` - Static image assets
- `media/` - User-uploaded files

## Tech Stack

- Python 3.12, Django 5.2, Wagtail 7.2
- uv for dependency management
- sentence-transformers + UMAP for article visualizations
- ruff for linting

## Commands

```bash
uv run manage.py runserver     # Dev server
uv run manage.py migrate       # Run migrations
uv run manage.py createsuperuser
```

## SEO

Preserve all existing SEO features and implement best practices.

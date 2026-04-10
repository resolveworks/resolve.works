# Resolve.

Source code of [resolve.works](https://resolve.works) — the site for **Resolve.**, an IT consulting practice helping ethical SMBs build modern software that saves time without replacing people.

Run by [Johan Schuijt](https://www.linkedin.com/in/johanschuijt/). Remote, Europe-focused, global clients welcome. If you have a data problem worth solving, [get in touch](https://resolve.works).

## Tech stack

- Python 3.12, Django 5.2, Wagtail 7.2
- [uv](https://docs.astral.sh/uv/) for dependency management
- sentence-transformers + UMAP for article visualizations
- ruff for linting

## Local development

```bash
uv sync
uv run manage.py migrate
uv run manage.py seed
uv run manage.py createsuperuser
uv run manage.py runserver
```

Frontend at http://localhost:8000, admin at http://localhost:8000/admin.

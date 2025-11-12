# Resolve.works

A consulting website built with Wagtail CMS.

## Setup

1. **Install dependencies** (requires [uv](https://docs.astral.sh/uv/)):
   ```bash
   uv sync
   ```

2. **Run migrations**:
   ```bash
   uv run python manage.py migrate
   ```

3. **Create a superuser**:
   ```bash
   uv run python manage.py createsuperuser
   ```

4. **Seed the homepage** (optional):
   ```bash
   uv run python manage.py seed_homepage
   ```

## Usage

**Development server**:
```bash
uv run python manage.py runserver
```

Visit:
- Frontend: http://localhost:8000
- Admin: http://localhost:8000/admin

**Docker** (production):
```bash
docker build -t resolve-works .
docker run -p 8000:8000 resolve-works
```

## Project Structure

- `home/` - Homepage app with StreamField blocks
- `resolve/` - Django project settings
- `index.html`, `styles.css`, `scripts.js` - Original static files (reference)

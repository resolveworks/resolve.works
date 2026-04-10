#!/bin/sh
set -e

uv run --no-dev manage.py collectstatic --noinput
exec uv run --no-dev gunicorn resolve.wsgi:application --bind 0.0.0.0:8000

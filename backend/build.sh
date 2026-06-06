#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Gather all admin and app static assets
python manage.py collectstatic --no-input

# Run migrations automatically on deploy
python manage.py migrate
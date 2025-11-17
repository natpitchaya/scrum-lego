#!/usr/bin/env bash
# Script to create Django superuser non-interactively

cd backend

# Set default values if environment variables are not set
DJANGO_SUPERUSER_USERNAME="${DJANGO_SUPERUSER_USERNAME:-admin}"
DJANGO_SUPERUSER_EMAIL="${DJANGO_SUPERUSER_EMAIL:-admin@yale.edu}"
DJANGO_SUPERUSER_PASSWORD="${DJANGO_SUPERUSER_PASSWORD:-changeme123}"

echo "Creating superuser: $DJANGO_SUPERUSER_USERNAME"

python manage.py createsuperuser \
    --noinput \
    --username "$DJANGO_SUPERUSER_USERNAME" \
    --email "$DJANGO_SUPERUSER_EMAIL" || echo "Superuser already exists or creation failed"

echo "Superuser creation completed"
echo "Login at: /admin/ with username: $DJANGO_SUPERUSER_USERNAME"

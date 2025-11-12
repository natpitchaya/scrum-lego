#!/usr/bin/env bash
# exit on error
set -o errexit

cd backend

pip install -r ../requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Fetch events - continue even if it fails
echo "Fetching events from Yale sources..."
python manage.py fetch_events || echo "Warning: fetch_events failed, but continuing deployment"

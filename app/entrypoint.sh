#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate --noinput
echo "Syncing data..."
python manage.py sync_rick_and_morty
echo "Starting server..."
exec "$@"

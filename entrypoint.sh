#!/bin/bash
set -e

# Run Django setup commands
python manage.py create_ahj_schema
python manage.py makemigrations
python manage.py migrate

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:8000 --workers 1 --threads 4 --timeout 120 genesis.wsgi:application

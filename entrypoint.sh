#!/bin/bash
python manage.py migrate
python manage.py collectstatic --noinput

# Prepare log files and output logs to stdout
mkdir -p /backend/logs/
touch /backend/logs/gunicorn.log
touch /backend/logs/access.log

echo Starting Gunicorn
python manage.py runserver 0.0.0.0:8000

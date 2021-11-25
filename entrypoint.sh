#!/bin/bash
python manage.py migrate
python manage.py collectstatic --noinput

# Prepare log files and output logs to stdout
mkdir -p /backend/logs/
touch /backend/logs/gunicorn.log
touch /backend/logs/access.log

echo Starting Gunicorn
exec gunicorn wsgi:application \
    --name backend \
    --bind unix:/backend/app.sock \
    --workers 3 \
    --log-level=info \
    --log-file=/backend/logs/gunicorn.log \
    --access-logfile=/backend/logs/access.log

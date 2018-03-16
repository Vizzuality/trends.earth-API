#!/bin/bash
set -e

case "$1" in
    develop)
        echo "Running Development Server"
        echo -e "$GCLOUD_STORAGE" | base64 -d > storage.json
        exec python main.py
        ;;
    test)
        echo "Test (not yet)"
        ;;
    start)
        echo "Running Start"
        exec gunicorn -c gunicorn.py gefapi.wsgi:application
        ;;
    worker)
        echo "Running celery"
        echo -e "$GCLOUD_STORAGE" | base64 -d > storage.json
        exec celery -A gefapi.celery worker -E -B --loglevel=DEBUG
        ;;
    *)
        exec "$@"
esac

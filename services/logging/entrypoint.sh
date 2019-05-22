#!/bin/sh

echo "waiting for postgres"

while ! nc -z logs-db 5432; do
    sleep 0.1
done

echo "Postgres started."

python manage.py run -h 0.0.0.0
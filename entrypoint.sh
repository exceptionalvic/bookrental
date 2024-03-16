#!/bin/sh

set -e

# Run Migrations
if [ "x$DJANGO_MANAGEPY_MIGRATE" = 'xon' ]; then
    python manage.py migrate --noinput
    echo "migration successful"
fi

# Run collectstatic
if [ "x$DJANGO_MANAGEPY_COLLECTSTATIC" = 'xon' ]; then
    python manage.py collectstatic --no-input;
    echo "collectstatic ran successfully"
fi

exec "$@"
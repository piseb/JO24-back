#!/bin/sh

# Migrations
./manage.py migrate --fake-initial --noinput

# Load Fixtures
fixtures="./apiv1/fixtures/*json"
for fixture in $fixtures; do
  ./manage.py loaddata $fixture
done

exec "$@"

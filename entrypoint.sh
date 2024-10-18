#!/bin/sh

# Migrations
./manage.py migrate --fake-initial --noinput

# Load Fixtures
fixtures="./api/fixtures/*json"
for fixture in $fixtures; do
  ./manage.py loaddata $fixture
done

exec "$@"

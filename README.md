# for local dev

- create `.env` (see `.env.example`)

## Docker postgres

```
$ docker volume create jo24-data
$ docker run -p 5432:5432 --name jo24-db -e POSTGRES_PASSWORD=jo24 -e POSTGRES_USER=jo24 -d --name jo24-back-DB -v pgdata-jo-24:/var/lib/postgresql/data postgres:15.4
```

- migrate : `./src/manage.py migrate`
- load the fixtures : `./src/manage.py loaddata ./src/apiv1/fixtures/*json`
- run local DJango in DEBUG mode : `./src/manage.py runserver`

# docker-flask-react-users

Backend users service for the [docker-flask-react](https://github.com/iyp-uk/docker-flask-react) project.

## Set up your IDE

So that it remembers some things for you, like:

* Image tag: `docker-flask-react-users`
* Container name: `docker-flask-react-users`
* Port mapping: `5000 -> 5000`
* Links: `postgres` (see below, you must run it first)
* Volume binding: current directory to `/usr/src/app`
* Environment variables
    * `APP_SETTINGS`: `app.config.DevelopmentConfig`
    * `DATABASE_URL`: `postgres://postgres:postgres@postgres:5432/app`
    * `TEST_DATABASE_URL`: `postgres://postgres:postgres@postgres_test:5432/app`

## Run it

First launch your database service:
```console
$ docker run --name postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=app -d postgres:alpine
```
And the one for tests:
```console
$ docker run --name postgres_test -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=app -d postgres:alpine
```

Then build and launch your container (through IDE is one click...)
```console
$ docker build -t docker-flask-react-users-service .
$ docker run -p 5000:5000 --name users --link postgres --link postgres_test -e APP_SETTINGS=app.config.DevelopmentConfig -e DATABASE_URL=postgres://postgres:postgres@postgres:5432/app -d docker-flask-react-users-service
```

You can eventually initialise the DB too:
```console
$ docker exec -it users python manage.py recreate_db
```

Or run the tests:
```console
$ docker exec -it users python manage.py test
```

From that point on, you're good to go!

## Test Coverage

```console
$ docker exec -it users python manage.py cov
```

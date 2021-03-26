# Quick start
- create .env file in /offline-messanger, with
```sh
####### Postgres
POSTGRES_PASSWORD=secret
POSTGRES_USER=postgres
POSTGRES_DB=offline_messenger
POSTGRES_HOST=pg_db:5432
####### Sanic
host=0.0.0.0
port=8000
workers=1
debug=True
```
- start docker-compose from /offline-messanger
```sh
docker-compose up
```


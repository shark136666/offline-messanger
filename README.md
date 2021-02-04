# Quick start
- create .env file in /np-final-project, with
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
- create .env file in /np-final-project/sanic, with
```sh
host=0.0.0.0
port=8000
workers=1
debug=True
dbname="user":"password"@pg_db:5432/"db name"
```
- start docker-compose
```sh
docker-compose up
```


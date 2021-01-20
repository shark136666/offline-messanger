# np-final-project
# Quick start
- create .env file in /np-final-project, with
```sh
POSTGRES_PASSWORD="password" 
POSTGRES_USER="user"
POSTGRES_DB="data base name"
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


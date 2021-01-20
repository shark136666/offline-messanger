echo "##### try create revision"
alembic revision -m "init database_table" --autogenerate
echo "##### try upgrade database"
alembic upgrade head
echo "Succes, but it is not exactly"


import os
from dotenv import load_dotenv, find_dotenv

load_dotenv()


class SQLiteConfig:
    name = os.getenv('dbname', 'db.sqlite')
    url = rf'sqlite:///{name}'


class PostgresConfig:
    # 'postgresql://scott:tiger@localhost:5432/mydatabase'
    password = os.getenv('POSTGRES_PASSWORD')
    user = os.getenv('POSTGRES_USER')
    name = os.getenv('POSTGRES_DB')
    host = os.getenv('POSTGRES_HOST')
    # name = os.getenv('dbname', 'postgres:mysecretpassword@localhost:5432/postgres')
    url = rf'postgresql://{user}:{password}@{host}/{name}'



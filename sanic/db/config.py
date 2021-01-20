import os
from dotenv import load_dotenv


class SQLiteConfig:
    name = os.getenv('dbname', 'db.sqlite')
    url = rf'sqlite:///{name}'


class PostgresConfig:
    # 'postgresql://scott:tiger@localhost:5432/mydatabase'
    name = os.getenv('dbname', 'postgres:mysecretpassword@localhost:5432/postgres')
    url = rf'postgresql://{name}'



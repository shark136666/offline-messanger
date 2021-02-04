import os
from dotenv import load_dotenv

load_dotenv()


class SQLiteConfig:
    name = os.getenv('dbname', 'db.sqlite')
    url = rf'sqlite:///{name}'


class PostgresConfig:
    password = os.getenv('POSTGRES_PASSWORD')
    user = os.getenv('POSTGRES_USER')
    name = os.getenv('POSTGRES_DB')
    host = os.getenv('POSTGRES_HOST')
    url = rf'postgresql://{user}:{password}@{host}/{name}'



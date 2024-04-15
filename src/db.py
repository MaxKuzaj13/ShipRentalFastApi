from os import environ
from fastapi import Request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

db_database = environ.get("POSTGRES_DB")
db_user = environ.get("POSTGRES_USER")
db_password = environ.get("POSTGRES_PASSWORD")
db_host = environ.get("POSTGRES_HOST")
db_port = environ.get("POSTGRES_PORT")


def get_db(request: Request):
    return request.state.db


SQLALCHEMY_DB_URL = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}'
engine = create_engine(SQLALCHEMY_DB_URL)
Base = declarative_base()

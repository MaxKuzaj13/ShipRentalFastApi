from fastapi import Request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


def get_db(request: Request):
    return request.state.db


# TODO add to ENV file
SQLALCHEMY_DB_URL = 'postgresql://user:password@localhost:6543/db'
engine = create_engine(SQLALCHEMY_DB_URL)
Base = declarative_base()

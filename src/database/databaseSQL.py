from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base


DATABASE_USER = "root"
DATABASE_PASSWORD = ""
DATABASE_HOST = "localhost"
DATABASE_PORT = "3306"
DATABASE_NAME = "users"


SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
with engine.connect() as connection:
    connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME};"))


SQLALCHEMY_DATABASE_URL_WITH_DB = f"{SQLALCHEMY_DATABASE_URL}/{DATABASE_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL_WITH_DB)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
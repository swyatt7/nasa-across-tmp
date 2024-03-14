# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker, Session

from ...across_config import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
ThisSession = sessionmaker(bind=engine)
session: Session = ThisSession()

class Base(DeclarativeBase):
    pass
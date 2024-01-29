from sqlalchemy import engine
from sqlalchemy.orm import Session, declarative_base

from db.config import Config

engine = engine.create_engine(Config().DB_URL)
session = Session(engine)

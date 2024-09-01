from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float
from os import getenv

engine = create_engine(f'mysql+mysqlconnector://{getenv("DB_USER")}:{getenv("DB_PASSWORD")}.@{getenv("DB_HOST")}/{"DB_NAME"}')

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    book_id = Column(Integer, primary_key=True, unique=True)
    title = Column(String)
    author = Column(String)
    current_lowest_price = Column(Float)
    link = Column(String)

Base.metadata.create_all(engine)

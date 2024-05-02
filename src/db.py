import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///data.db")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    customer_username = Column(String(100), nullable=False)
    title = Column(String(250), nullable=False)
    mark = Column(Integer, nullable=False)
    immediately = Column(Boolean, default=False, nullable=False)
    price = Column(Integer, nullable=False)
    email = Column(String(100), nullable=False)
    comment = Column(String(1000), nullable=True)
    message_id = Column(Integer, nullable=False, unique=True)
    confirm_date = Column(DateTime, default=sqlalchemy.func.now())
    released = Column(Boolean, default=False)
    release_date = Column(DateTime, nullable=True)

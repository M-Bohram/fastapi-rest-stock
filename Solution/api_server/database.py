from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://postgres:example@db:5432/postgres', echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class UserStocks(Base):
    __tablename__ = 'user_stocks'
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    stock_id = Column(String, ForeignKey('stocks.stock_id'), primary_key=True)
    name = Column(String(50))
    number = Column(Integer)
    stock = relationship("Stock", back_populates="users")
    user = relationship("User", back_populates="stocks")

class Stock(Base):
    __tablename__ = 'stocks'

    # id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(String, primary_key=True, index=True)
    name = Column(String(50))
    current_price = Column(Integer)
    availability = Column(Integer)
    day_highest_price = Column(Integer)
    day_lowest_price = Column(Integer)
    hour_highest_price = Column(Integer)
    hour_lowest_price = Column(Integer)
    updated_at = Column(DateTime)
    users = relationship("UserStocks", back_populates="stock")


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    balance = Column(Integer)
    stocks = relationship("UserStocks", back_populates="user")



Base.metadata.create_all(engine)
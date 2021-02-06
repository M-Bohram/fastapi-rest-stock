from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://postgres:example@db:5432/postgres', echo=False)

Session = sessionmaker(bind=engine)

session = Session()

Base = declarative_base()

class Stock(Base):
    __tablename__ = 'stocks'

    stock_id = Column(String, primary_key=True, index=True)
    name = Column(String(50))
    current_price = Column(Integer)
    availability = Column(Integer)
    day_highest_price = Column(Integer)
    day_lowest_price = Column(Integer)
    hour_highest_price = Column(Integer)
    hour_lowest_price = Column(Integer)
    updated_at = Column(DateTime)

Base.metadata.create_all(engine)
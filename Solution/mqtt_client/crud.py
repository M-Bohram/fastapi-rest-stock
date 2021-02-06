
from database import session, Stock
from utils import get_datetime_from_timestamp, get_day_hour_from_timestamp

def create_db_stock_instance(stock):
    db_stock = Stock(stock_id=stock.stock_id, name=stock.name,\
         current_price=stock.current_price, availability=stock.availability,\
         hour_highest_price=stock.hour_highest_price,\
         hour_lowest_price=stock.hour_lowest_price,\
         day_highest_price=stock.day_highest_price, \
         day_lowest_price=stock.day_lowest_price, updated_at=stock.updated_at)
    session.add(db_stock)
    session.commit()


def update_db_stock_instance(stock):
    db_stock = get_db_stock_instance(stock.stock_id)
    db_stock.current_price = stock.price
    db_stock.availability = stock.availability
    db_stock_day, db_stock_hour = get_day_hour_from_timestamp(db_stock.updated_at)
    stock_day, stock_hour = get_day_hour_from_timestamp(stock.timestamp)
    if db_stock_day != stock_day:
        db_stock.day_highest_price = stock.price
        db_stock.day_lowest_price = stock.price
    else:
        if stock.price > db_stock.day_highest_price:
            db_stock.day_highest_price = stock.price
        elif stock.price < db_stock.day_lowest_price:
            db_stock.day_lowest_price = stock.price
    if db_stock_hour != stock_hour:
        db_stock.hour_highest_price = stock.price
        db_stock.hour_lowest_price = stock.price
    else:
        if stock.price > db_stock.hour_highest_price:
            db_stock.hour_highest_price = stock.price
        elif stock.price < db_stock.hour_lowest_price:
            db_stock.hour_lowest_price = stock.price
    db_stock.updated_at = get_datetime_from_timestamp(stock.timestamp)
    session.commit()


def get_db_stocks():
    return session.query(Stock).all()


def get_db_stock_instance(stock_id):
    return session.query(Stock).filter(Stock.stock_id == stock_id).first()


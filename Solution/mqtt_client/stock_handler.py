from datetime import datetime as dt
from crud import get_db_stock_instance, get_db_stocks, update_db_stock_instance, create_db_stock_instance

# stocks = []

class StockClass():
    stock_id = ''
    name = ''
    price = 0
    availability = 0
    timestamp = ''


def update_stock(stock):
    update_db_stock_instance(stock)


def add_stock(stock):
    new_stock = StockClass()
    new_stock.stock_id = stock.stock_id
    new_stock.name = stock.name
    new_stock.current_price = stock.price
    new_stock.availability = stock.availability
    new_stock.hour_highest_price = stock.price
    new_stock.hour_lowest_price = stock.price
    new_stock.day_highest_price = stock.price
    new_stock.day_lowest_price = stock.price
    new_stock.updated_at = stock.timestamp
    print(new_stock)
    create_db_stock_instance(new_stock)


def get_day_hour_from_timestamp(timestamp):
    if type(timestamp) == str:
        timestamp = dt.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    day = timestamp.day
    hour = timestamp.hour
    return day, hour


def add_or_update_stock(stock):
    db_stocks = get_db_stocks()
    stock_exists = False
    for db_stock in db_stocks:
        if stock.stock_id == db_stock.stock_id:
            stock_exists = True
            update_stock(stock)
            break
    if not stock_exists:
        add_stock(stock)


def convert_incoming_stock(stock):
    new_stock = StockClass()
    new_stock.stock_id = stock['stock_id']
    new_stock.name = stock['name']
    new_stock.price = stock['price']
    new_stock.availability = stock['availability']
    new_stock.timestamp = stock['timestamp']
    return new_stock
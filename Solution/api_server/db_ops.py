from sqlalchemy.orm import Session
from database import Stock, User, UserStocks


#status codes as constants for readability
STOCKS_NOT_ENOUGH = 1
PRICE_NOT_WITHIN_LIMITS = 2
BALANCE_NOT_ENOUGH = 3
USER_NOT_FOUND = 4

def get_stock(stock_id: str, db: Session):
    return db.query(Stock).filter(Stock.stock_id == stock_id).first()


def get_stocks(db: Session):
    return db.query(Stock).all()


def get_users(db: Session):
    users = db.query(User).all()
    for user in users:
        print("user stocks", user.stocks)
    return users


def get_user(user_id: int, db: Session):
    return db.query(User).filter(User.user_id == user_id).first()
    
    

def convert_user_to_json(db_user):
    user = {}
    user['user_id'] = db_user.user_id
    user['name'] = db_user.name
    user['balance'] = db_user.balance
    user['stocks'] = []
    for stock in db_user.stocks:
        new_stock = {}
        new_stock['stock_id'] = stock.stock_id
        new_stock['name'] = stock.name
        new_stock['number'] = stock.number
        user['stocks'].append(new_stock)
    return user

def create_user(name: str, balance: int, db: Session):
    user = User(name=name, balance=balance)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def add_fund(user_id: int, amount: int, db: Session):
    user = get_user(user_id, db)
    if not user:
    	return USER_NOT_FOUND
    user.balance += amount
    db.commit()

def widthraw(user_id: int, amount: int, db: Session):
    user = get_user(user_id, db)
    if not user:
    	return USER_NOT_FOUND
    if user.balance < amount:
        return BALANCE_NOT_ENOUGH
    user.balance -= amount
    db.commit()


# I returned codes because this module should be handling db operations
# and return status or db objects and not the json object to the user
def buy_stocks(user_id: int, stock_id: str, total: int, upper_bound: int, lower_bound: int, db: Session):
    user = get_user(user_id, db)
    stock = get_stock(stock_id, db)
    if not stock.availability >= total:
        return STOCKS_NOT_ENOUGH
    if stock.current_price > upper_bound or stock.current_price < lower_bound:
        return PRICE_NOT_WITHIN_LIMITS
    stocks_cost = total * stock.current_price
    if user.balance < stocks_cost:
        return BALANCE_NOT_ENOUGH
    stock.availability -= total
    user.balance -= total * stock.current_price
    for user_stock in user.stocks:
        if user_stock.stock_id == stock.stock_id:
            user_stock.number += total
            user_stock.user_id = user.user_id
            db.commit()
            return
    user_stocks = UserStocks(name=stock.name, number=total)
    user_stocks.stock = stock
    user.stocks.append(user_stocks)
    db.commit()




def sell_stocks(user_id: int, stock_id: str, total: int, upper_bound: int, lower_bound: int, db: Session):
    user = get_user(user_id, db)
    stock = get_stock(stock_id, db)
    print(stock.current_price)
    for user_stock in user.stocks:
        if user_stock.stock_id == stock_id and user_stock.number < total:
            return STOCKS_NOT_ENOUGH
    if stock.current_price > upper_bound or stock.current_price < lower_bound:
        return PRICE_NOT_WITHIN_LIMITS
    stocks_cost = total * stock.current_price
    user.balance += stocks_cost
    stock.availability += total
    for user_stock in user.stocks:
        if user_stock.stock_id == stock_id:
            user_stock.number -= total
            if user_stock.number == 0:
                user.stocks.remove(stock)
    db.commit()

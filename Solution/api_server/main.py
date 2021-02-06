
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import db_ops, schemas
import time

app = FastAPI()

# to make sure the DB container is initialized, not best solution though
time.sleep(10)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


############################     Required APIs  ############################

@app.post("/stock", tags=["Required"])
def get_stock(stock_id: schemas.GetStock, db: Session = Depends(get_db)):
    stock = db_ops.get_stock(stock_id, db)
    if not stock:
        raise HTTPException(status_code=404, detail="stock not found")
    return stock


@app.post("/user", tags=["Required"])
def get_user(user_id: schemas.GetUser, db: Session = Depends(get_db)):
    user = db_ops.get_user(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    user = db_ops.convert_user_to_json(user)
    return user


@app.post("/deposit", tags=["Required"])
def add_fund(deposit: schemas.Deposit, db: Session = Depends(get_db)):
    code = db_ops.add_fund(deposit.user_id, deposit.amount, db)
    if code == db_ops.USER_NOT_FOUND:
    	raise HTTPException(status_code=404, detail="user not found")
    return { "message": "success" }

@app.post("/withdraw", tags=["Required"])
def withraw(withdraw: schemas.Withdraw, db: Session = Depends(get_db)):
    code = db_ops.widthraw(withdraw.user_id, withdraw.amount, db)
    if code == db_ops.BALANCE_NOT_ENOUGH:
        raise HTTPException(status_code=409, detail="the user balance is not enough to complete the transaction")
    elif code == db_ops.USER_NOT_FOUND:
    	raise HTTPException(status_code=404, detail="user not found")
    return { "message": "success" }


@app.post("/buy", tags=["Required"])
def buy_stocks(buy_stock: schemas.BuyStock, db: Session = Depends(get_db)):
    code = db_ops.buy_stocks(buy_stock.user_id, buy_stock.stock_id, buy_stock.total, buy_stock.upper_bound, buy_stock.lower_bound, db)
    if code == db_ops.STOCKS_NOT_ENOUGH:
        raise HTTPException(status_code=409, detail="the number of available stocks was lower than the required")
    elif code == db_ops.PRICE_NOT_WITHIN_LIMITS:
        raise HTTPException(status_code=409, detail="the price was beyond the limits")
    elif code == db_ops.BALANCE_NOT_ENOUGH:
        raise HTTPException(status_code=409, detail="the user does not have enough cash")
    return { "message": "success" }


@app.post("/sell", tags=["Required"])
def sell_stocks(sell_stock: schemas.SellStock, db: Session = Depends(get_db)):
    code = db_ops.sell_stocks(sell_stock.user_id, sell_stock.stock_id, sell_stock.total, sell_stock.upper_bound, sell_stock.lower_bound, db)
    if code == db_ops.STOCKS_NOT_ENOUGH:
        raise HTTPException(status_code=409, detail="the user does not have enough stocks to complete the transaction")
    elif code == db_ops.PRICE_NOT_WITHIN_LIMITS:
        raise HTTPException(status_code=409, detail="the price was beyond the limits")
    return { "message": "success" }



############################     APIs for testing   ############################

@app.get("/stocks", tags=["Testing"])
def get_stocks(db: Session = Depends(get_db)):
    return db_ops.get_stocks(db)

@app.post("/users", tags=["Testing"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db_ops.create_user(user.name, user.amount, db)
    return { "user", user }

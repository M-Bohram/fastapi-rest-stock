
from typing import List
from pydantic import BaseModel
from datetime import datetime

class GetStock(BaseModel):
    stock_id: str

class GetUser(BaseModel):
    user_id: int

class Deposit(BaseModel):
    user_id: int
    amount: int

class Withdraw(Deposit):
    pass

class BuyStock(BaseModel):
    user_id: int
    stock_id: str
    total: int
    upper_bound: int
    lower_bound: int

class SellStock(BuyStock):
    pass


class Stock(BaseModel):
    id: int
    stock_id: str
    name: str
    current_price: int
    availability: int
    day_highest_price: int
    day_lowest_price: int
    hour_highest_price: int
    hour_lowest_price: int
    updated_at: datetime


class UserStocks(BaseModel):
    stock_id: str
    name: str
    number: int
    user_id: int


class User(BaseModel):
    user_id: int
    name: str
    balance: int
    stocks: List[UserStocks]


class UserCreate(BaseModel):
    name: str
    amount: int
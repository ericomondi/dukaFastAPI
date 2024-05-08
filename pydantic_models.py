from pydantic import BaseModel
from datetime import datetime

class CreateUserRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class ProductsBase(BaseModel):
    name: str
    cost: int
    price: int
    img_url: str
    stock_quantity: int



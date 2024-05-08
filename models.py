from sqlalchemy import Boolean, Column, Integer, String,func, DateTime, DECIMAL, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    hashed_password = Column(String(256))
    created_at = Column(DateTime, default=func.now())


    products = relationship("Products", back_populates="user")

class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False ,index=True)
    cost = Column(DECIMAL(14, 2), nullable=False)
    price = Column(DECIMAL(14, 2) ,nullable=False)
    img_url = Column(String(100))
    stock_quantity = Column(DECIMAL(14, 2), nullable=False)
    created_at = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("Users", back_populates="products")



# Define ORM models for the database
# Related files: db2.py, crud.py

from sqlalchemy import Column, Integer, String, Float
from db2 import Base

class Item(Base):
    """
    ORM model representing the 'items' table in the database.
    Attributes:
        id: Primary key, auto-incremented integer
        name: Name of the item (string), must be unique
        price: Price of the item (float)
        quantity: Number of items in stock, default is 0
    """
    __tablename__= "items"

    id= Column(Integer, primary_key=True, index=True)
    name= Column(String(50), unique=True, nullable=False, index=True)
    price= Column(Float, nullable=False)
    quantity= Column(Integer, default=0) # Default quantity to 0 if not provided

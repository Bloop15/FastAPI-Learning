### Connect MySQL DB with FastAPI
# We will use a free MySQL server from FreeSQLDatabase for testing purposes.

# MySQL connection URL format:
# mysql+pymysql://<username>:<password>@<host>:<port>/<database>
mysql_url= "mysql+pymysql://sql12804329:EgVn6FxZet@sql12.freesqldatabase.com:3306/sql12804329"

# Required library to connect FastAPI/SQLModel to MySQL:
# pip install pymysql

from fastapi import FastAPI
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, List
from contextlib import asynccontextmanager


# -------------------------------
# Create SQLModel Engine for MySQL
# -------------------------------
# echo=True prints all SQL queries in the console, useful for debugging
engine= create_engine(mysql_url, echo=True)


# -------------------------------
# Define the SQLModel for the 'items' table
# -------------------------------
class Item(SQLModel, table=True):
    """
    This model represents the 'items' table in the MySQL database.
    Attributes:
        id: Primary key, auto-incremented integer
        name: Name of the item (string)
        price: Price of the item (float)
        is_offer: Boolean flag to indicate if the item has an offer, default False
    """
    id: Optional[int]= Field(default=None, primary_key=True)
    name: str
    price: float
    is_offer: bool=False


# -------------------------------
# Function to create database tables
# -------------------------------
def create_db_and_tables():
    """
    Creates all tables defined with SQLModel.metadata in the MySQL database.
    Ensures that the database schema exists before using the app.
    """
    SQLModel.metadata.create_all(engine)


# -------------------------------
# FastAPI App with Lifespan Event
# -------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan function is called on startup and shutdown of the app.
    On startup: create database tables.
    On shutdown: nothing needed here.
    """
    create_db_and_tables()
    yield

# Pass the lifespan function to FastAPI
app=FastAPI(lifespan=lifespan)


# -------------------------------
# POST Endpoint to Create Item
# -------------------------------
@app.post("/items/")
def create_item(item: Item):
    """
    Adds a new item to the MySQL database.
    Steps:
    1. Open a database session
    2. Add the new item
    3. Commit the transaction
    4. Refresh the item to get auto-generated fields (like id)
    5. Return the item
    """
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item


# -------------------------------
# GET Endpoint to Read All Items
# -------------------------------
@app.get("/items/", response_model=List[Item])
def read_items():
    """
    Fetches all items from the MySQL database.
    Steps:
    1. Open a database session
    2. Select all items using SQLModel's select()
    3. Convert the result to a list and return
    """
    with Session(engine) as session:
        items= session.exec(select(Item)).all()
        return items

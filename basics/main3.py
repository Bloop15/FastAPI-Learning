### Connect FastAPI to an SQL Database
# We need to install sqlmodel to do this
# pip install sqlmodel

from sqlmodel import SQLModel, Field
from typing import Optional
from contextlib import asynccontextmanager


# -------------------------------
# Define the SQLModel for our table
# -------------------------------
class Item(SQLModel, table=True):
    """
    This model represents the 'items' table in the database.
    Attributes:
        id: Primary key, auto-incremented integer
        name: Name of the item (string)
        price: Price of the item (float)
        is_offer: Boolean flag to indicate if item has an offer, default False
    """
    id: Optional[int]= Field(default=None, primary_key=True)
    name: str
    price: float
    is_offer: bool=False


# -------------------------------
# Setup SQLite Database Engine
# -------------------------------
from sqlmodel import create_engine, Session

# SQLite file name and connection URL
sqlite_file_name= "database.db"
sqlite_url= f"sqlite:///{sqlite_file_name}"

# Create a SQLModel engine to connect to the database
# echo=True prints all SQL statements to the console for debugging
engine= create_engine(sqlite_url, echo=True)


# -------------------------------
# Function to create database and tables
# -------------------------------
def create_db_and_tables():
    """
    Creates all tables defined with SQLModel.metadata.
    This is called on app startup to ensure tables exist before using them.
    """
    SQLModel.metadata.create_all(engine)


# -------------------------------
# FastAPI App with Lifespan Event
# -------------------------------
from fastapi import FastAPI

# Lifespan function is called on app startup and shutdown
# We use asynccontextmanager to manage async lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    On startup: create DB and tables.
    On shutdown: nothing to do here.
    """
    create_db_and_tables()
    yield
    # code after yield would run on shutdown (none here)


# Pass the lifespan function to FastAPI
app= FastAPI(lifespan=lifespan)


# -------------------------------
# Dependency Injection (optional for later use)
# -------------------------------
from fastapi import Depends


# -------------------------------
# POST Endpoint to Create Item
# -------------------------------
@app.post("/items/")
def create_item(item: Item):
    """
    Adds a new item to the database.
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
from typing import List
from sqlmodel import select

@app.get("/items/", response_model=List[Item])
def read_items():
    """
    Fetches all items from the database.
    Steps:
    1. Open a database session
    2. Select all items using SQLModel's select()
    3. Convert the result to a list and return
    """
    with Session(engine) as session:
        items= session.exec(select(Item)).all()
        return items


# -------------------------------
# Notes:
# -------------------------------
# 1. SQLModel combines Pydantic models and SQLAlchemy models, so the same class can be used for validation and database operations.
# 2. Using the lifespan function ensures tables are created automatically when the app starts, so we don't have to manually run create_all().
# 3. `Session` manages transactions; always commit after adding/updating items.
# 4. response_model ensures that FastAPI automatically converts database objects to JSON responses.

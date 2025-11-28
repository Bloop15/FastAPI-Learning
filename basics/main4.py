### Connect Postgres DB with FastAPI
# In this example, we use Supabase, which provides a free hosted PostgreSQL database.

# PostgreSQL connection URL format:
# postgresql://<username>:<password>@<host>:<port>/<database>?sslmode=require

postgres_url = "postgresql://postgres:FastAPI123@db.jtajxuoryfjchbpqhhrj.supabase.co:5432/postgres?sslmode=require"

# Required library to connect FastAPI/SQLModel to PostgreSQL:
# pip install psycopg2-binary

from sqlmodel import SQLModel, Field
from typing import Optional


# -------------------------------
# Define the SQLModel for our table
# -------------------------------
class Item(SQLModel, table=True):
    """
    This model represents the 'items' table in the PostgreSQL database.
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
# Setup PostgreSQL Engine
# -------------------------------
from sqlmodel import create_engine, Session

# Create an SQLModel engine for connecting to PostgreSQL
# echo=True prints all SQL statements to the console for debugging
engine= create_engine(postgres_url, echo=True)


# -------------------------------
# FastAPI App with Lifespan Event
# -------------------------------
from fastapi import FastAPI
from contextlib import asynccontextmanager

def create_db_and_tables():
    """
    Create all tables defined with SQLModel.metadata in the PostgreSQL database.
    Ensures that the database schema is set up before using the app.
    """
    SQLModel.metadata.create_all(engine)

# Lifespan function runs on app startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    On startup: create database tables.
    On shutdown: nothing to do here.
    """
    create_db_and_tables()
    yield

# Pass the lifespan function to FastAPI
app=FastAPI(lifespan=lifespan)

@app.post("/items/")
def create_item(item: Item):
    """
    Adds a new item to the PostgreSQL database.
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
    Fetch all items from the PostgreSQL database.
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
# 1. SQLModel works with multiple databases (SQLite, PostgreSQL, MySQL) using the same model.
# 2. Using the lifespan function ensures tables are created automatically when the app starts.
# 3. `Session` manages transactions; always commit after adding/updating items.
# 4. response_model ensures that FastAPI automatically converts database objects to JSON responses.
# 5. echo=True is very helpful for debugging SQL queries while learning.

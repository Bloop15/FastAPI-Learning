### Main FastAPI application file for User Authentication
# Related files:
#   - db.py      -> database configuration
#   - models.py  -> SQLAlchemy table definitions
#   - schemas.py -> Pydantic models for request validation

from fastapi import FastAPI, HTTPException
from passlib.context import CryptContext
from db import database, metadata, engine
from models import users
from schemas import UserCreate, UserLogin


# -------------------------------
# FastAPI Instance
# -------------------------------
app= FastAPI()


# -------------------------------
# Create the Table
# -------------------------------
# Creates all tables defined in models.py (here, the 'users' table)
metadata.create_all(engine)


# -------------------------------
# Password Context
# -------------------------------
# passlib CryptContext is used to hash and verify passwords securely
pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")


# -------------------------------
# Startup and Shutdown Events
# -------------------------------
@app.on_event("startup")
async def startup():
    # Connect to the database when app starts
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    # Disconnect from the database when app shuts down
    await database.disconnect()


# -------------------------------
# POST Endpoint: Register User
# -------------------------------
@app.post("/register")
async def register(user: UserCreate):
    """
    Registers a new user.
    1. Checks if username already exists.
    2. Validates password length (<=72 chars for bcrypt).
    3. Hashes the password before storing in the database.
    4. Inserts the user into the 'users' table.
    """
    # Check if user already exists
    query= users.select().where(users.c.username==user.username)
    existing_user= await database.fetch_one(query)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Validate password length (bcrypt limitation)
    if len(user.password.encode("utf-8")) > 72:
        raise HTTPException(status_code=400, detail="Password too long. Must be ≤ 72 characters.")
    
    # Hash the password
    hashed_password= pwd_context.hash(user.password)

    # Insert the user into the database
    query= users.insert().values(username=user.username, password=hashed_password)
    await database.execute(query)

    return {"message": "User registered successfully"}


# -------------------------------
# POST Endpoint: Login User
# -------------------------------
@app.post("/login")
async def login(user: UserLogin):
    """
    Logs in an existing user.
    1. Fetches the user by username.
    2. Verifies the provided password against the hashed password in DB.
    3. Returns success or error message.
    """
    # Check if user exists
    query= users.select().where(users.c.username==user.username)
    existing_user= await database.fetch_one(query)
    if not existing_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    # Verify password
    if not pwd_context.verify(user.password, existing_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    return {"message": "Login Successfull!"}

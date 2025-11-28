# Demonstrates JWT Authentication in FastAPI
# Related files:
#   - database2.py   -> Database connection and ORM base
#   - models3.py     -> User model for authentication
#   - auth_utils.py  -> Utility functions for password hashing, JWT creation/validation

# Install dependencies:
# pip install python-jose passlib[bcrypt] fastapi sqlalchemy

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database2 import SessionLocal, engine, Base
from models3 import User
from auth_utils import create_access_token, decode_access_token, verify_password, hash_password
from pydantic import BaseModel
from fastapi.security import HTTPBearer


# -------------------------------
# Database: Create tables
# -------------------------------
Base.metadata.create_all(bind=engine)


# -------------------------------
# FastAPI Instance
# -------------------------------
app= FastAPI()
security= HTTPBearer()  # HTTP Bearer for token-based auth


# -------------------------------
# Dependency: Get DB session
# -------------------------------
def get_db():
    """
    Provide a database session to endpoints.
    Ensures session is closed after request.
    """
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------
# Pydantic Model: User Input
# -------------------------------
class UserCreate(BaseModel):
    username: str
    password: str


# -------------------------------
# Signup Endpoint
# -------------------------------
@app.post("/signup")
def signup(user: UserCreate, db: Session= Depends(get_db)):
    """
    Create a new user with hashed password.
    - Checks if username already exists
    - Returns user info (id and username)
    """
    existing= db.query(User).filter(User.username==user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered!")
    
    hashed_password= hash_password(user.password)
    new_user= User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"username": new_user.username, "id": new_user.id}


# -------------------------------
# Login Endpoint
# -------------------------------
@app.post("/login")
def login(user: UserCreate, db: Session= Depends(get_db)):
    """
    Login endpoint:
    - Verifies username and password
    - Returns a JWT access token if successful
    """
    db_user= db.query(User).filter(User.username==user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials!")
    
    access_token= create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer", "user": db_user}


# -------------------------------
# Protected Route Example
# -------------------------------
from typing import Optional
from fastapi import Header, status
from fastapi.security import HTTPAuthorizationCredentials

@app.get("/protected")
def protected_route(credentials: HTTPAuthorizationCredentials= Depends(security)):
    """
    Example protected route that requires a valid JWT token.
    - Extracts token from Authorization header
    - Decodes and validates JWT
    - Returns payload info if valid
    """
    if not credentials: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials missing!!")
    
    token= credentials.credentials
    payload= decode_access_token(token)

    if not payload:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token!!")
    
    return {"message": "Protected route accessed!", "user": payload["sub"]}

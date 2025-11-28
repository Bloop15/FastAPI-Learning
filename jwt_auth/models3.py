# Defines User model for JWT Authentication
# Related files: database2.py

from database2 import Base, engine, SessionLocal
from sqlalchemy import Column, Integer, String

class User(Base):
    """
    SQLAlchemy model for users.
    - username: unique identifier for login
    - hashed_password: stores password securely
    """
    __tablename__= "users1"

    id= Column(Integer, primary_key=True, index=True)
    username= Column(String, unique=True, index=True)
    hashed_password= Column(String)

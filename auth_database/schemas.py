# Pydantic models for request validation
# Related file: app.py uses these for register/login endpoints

from pydantic import BaseModel

# Schema for creating a new user
class UserCreate(BaseModel):
    username: str
    password: str

# Schema for user login
class UserLogin(BaseModel):
    username: str
    password: str

# Notes:
# - UserCreate and UserLogin are identical here, but could differ in real apps.
#   Example: UserCreate may include email, phone number, etc., while UserLogin only needs username & password.

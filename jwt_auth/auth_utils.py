# Utility functions for authentication
# Related files: jwt.py

# Install dependencies:
# pip install python-jose passlib[bcrypt]

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta


# JWT config
SECRET_KEY= 'secret'
ALGORITHM= 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES= 30

# Password hashing context
pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")


# -------------------------------
# Password utilities
# -------------------------------
def hash_password(password: str):
    """Hash password for storing in DB."""
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """Verify plain password against hashed version."""
    return pwd_context.verify(plain_password, hashed_password)


# -------------------------------
# JWT utilities
# -------------------------------
def create_access_token(data: dict, expires_delta: timedelta= None):
    """Create JWT token with expiration."""
    to_encode= data.copy()
    expire= datetime.utcnow()+ (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt= jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """Decode JWT token and return payload; None if invalid."""
    try:
        payload= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

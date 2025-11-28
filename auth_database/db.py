# Database configuration file
# Related file: app.py (main FastAPI app uses this database)

from sqlalchemy import create_engine, MetaData
from databases import Database

# SQLite database URL
DATABASE_URL= "sqlite:///./users.db" # Example SQLite Database URL

# Database instance for async queries
database= Database(DATABASE_URL)

# Metadata object to hold table schemas (from models.py)
metadata= MetaData()

# SQLAlchemy engine for creating tables synchronously
engine= create_engine(DATABASE_URL)

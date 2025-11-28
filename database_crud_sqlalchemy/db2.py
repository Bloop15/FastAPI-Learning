# Database configuration file for CRUD APIs
# Related files: models2.py, crud.py

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database URL
DATABASE_URL= "sqlite:///./items.db"


# Create SQLAlchemy engine
# check_same_thread=False is needed for SQLite when using multiple threads
engine= create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Base class for our ORM models
Base= declarative_base()

# SessionLocal class to create session objects for DB operations
# autocommit=False ensures we manually commit transactions
# autoflush=False avoids automatic flush of pending changes until commit
SessionLocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)

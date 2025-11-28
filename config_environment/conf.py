# Configuration file using Pydantic Settings and environment variables
# Related files: environ.py, .env

# Install dependencies:
#   pip install pydantic-settings python-dotenv

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os


# Load variables from the .env file into environment
load_dotenv() # Reads .env and sets environment variables in os.environ


# -------------------------------
# Define Configuration Class
# -------------------------------
class Settings(BaseSettings):
    """
    Holds all application configuration variables.
    - database_url: URL for connecting to the database
    - secret_key: Secret key used for signing tokens, encryption, etc.
    """
    database_url: str= os.getenv('DATABASE_URL')
    secret_key: str= os.getenv('SECRET_KEY')

# Create a single settings instance to use across the application
settings= Settings()

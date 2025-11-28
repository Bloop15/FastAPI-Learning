# Demonstrates using the configuration settings in a FastAPI app
# Related files: conf.py, .env

from fastapi import FastAPI
from conf import settings  # Import the settings instance

app= FastAPI()

# Print database URL to confirm settings are loaded
print(settings.database_url)


# -------------------------------
# GET Endpoint: Display Config
# -------------------------------
@app.get("/")
async def root():
    """
    Returns configuration values as JSON.
    NOTE: Returning secret_key like this is only for demonstration!
    Never expose secrets in a real app.
    """
    return {"db_url": settings.database_url, "secret_key": settings.secret_key}

from fastapi import FastAPI

# Create an instance of the FastAPI class
# This instance will be used to define all our routes and configurations
app= FastAPI()

# -------------------------------
# Basic Route
# -------------------------------
@app.get("/")  # HTTP GET method at the root path "/"
def read_root():
    # Returns a simple JSON response
    return {"Hello": "World"}
 

# -------------------------------
# Dynamic Endpoints using Path and Query Parameters
# -------------------------------
@app.get("/items/{item_id}")  # Dynamic route using a path parameter
def read_item(item_id: int, q: str=None):
    """
    Path Parameter:
        item_id: An integer extracted from the URL
    Query Parameter:
        q: Optional string, can be passed after '?' in URL
    Example URL: /items/5?q=test
    """
    return {"item_id": item_id, "query": q}

# Notes:
# - FastAPI automatically validates the type of path parameters.
# - If you pass a wrong type (e.g., string for item_id), FastAPI will return a 422 Unprocessable Entity error.
# - Even if you pass a numeric string like "123", FastAPI will convert it to int.
# - Query parameters are optional by default. Here 'q' is optional with default None.
# - They are passed after '?' in the URL, like: /items/23?q=hello


# -------------------------------
# Optional Typed Query Parameters
# -------------------------------
@app.get("/products/")
def list_products(skip: int=0, limit: int=10):
    """
    Query Parameters:
        skip: Number of items to skip, default is 0
        limit: Maximum number of items to return, default is 10
    Example URL: /products/?skip=5&limit=20
    """
    return {"skip": skip, "limit": limit}

# Notes:
# - FastAPI automatically converts query parameters to the specified type.
# - Default values are used if parameters are not provided in the URL.
# - You can change these values by providing them in the URL query string.

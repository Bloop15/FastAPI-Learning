# Demonstrates custom exception handling in FastAPI
# Related concepts:
#   - HTTPException: built-in exception for HTTP errors
#   - Custom Exception classes
#   - Exception handlers for returning custom responses

from fastapi import FastAPI, HTTPException


# -------------------------------
# FastAPI Instance
# -------------------------------
app= FastAPI()


# -------------------------------
# Example: Handling Division by Zero
# -------------------------------
@app.get("/divide/")
def divide(a: float, b: float):
    """
    Divide two numbers.
    - If b == 0, raises a standard HTTPException with status 400
    """
    if b==0:
        raise HTTPException(status_code=400, detail="Division by zero is not allowed!")
    return {"result": a/b}


# -------------------------------
# Custom Exception Class
# -------------------------------
class NotFoundException(Exception):
    def __init__(self, name:str):
        """
    Custom exception for cases when an item is not found.
    - name: Name of the item that caused the exception
    """
        self.name= name


# -------------------------------
# Custom Exception Handler
# -------------------------------
from fastapi.responses import JSONResponse
from fastapi.requests import Request

@app.exception_handler(NotFoundException)
def not_found_exception_handler(request: Request, exc: NotFoundException):
    """
    Handles NotFoundException globally.
    - Returns JSON with status 404 and a custom message.
    """
    return JSONResponse(
        status_code=404,
        content={"message": f"{exc.name} not found!"}
    )


# -------------------------------
# Example Data Store
# -------------------------------
# Simple in-memory dictionary to simulate a database
items= {'apple':10, 'banana':20, 'orange':30}


# -------------------------------
# GET Endpoint: Fetch Item
# -------------------------------
@app.get("/items/{item_name}")
def get_item(item_name: str):
    """
    Fetches the quantity of an item.
    - If item_name is not in 'items', raises NotFoundException
    - Otherwise, returns item_name and quantity
    """
    if item_name not in items:
        raise NotFoundException(name=item_name)
    return {"item_name": item_name, "quantity": items[item_name]}

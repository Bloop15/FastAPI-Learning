### Post Requests (How to send and validate data in the API using Pydantic Models)

# Pydantic models are used to define classes that represent the structure of data sent to or returned from API endpoints. 
# They automatically validate the data types and structure, ensuring that incoming data is correct before it reaches your endpoint logic.

from fastapi import FastAPI
from pydantic import BaseModel

# Create FastAPI instance
app= FastAPI()


# -------------------------------
# Define Pydantic Model for Request
# -------------------------------
class Item(BaseModel):
    """
    This model defines the structure of the data expected in POST requests.
    Attributes:
        name: Name of the item (string)
        price: Price of the item (float)
        is_offer: Optional boolean to indicate if item has an offer, default is False
        password: Default string, used as an example of a field we may not want to return in responses
    """
    name: str
    price: float
    is_offer: bool = False
    password: str = "Don't show this"


# -------------------------------
# Define Pydantic Model for Response
# -------------------------------
class ItemResponse(BaseModel):
    """
    Response model to customize what is sent back to the client.
    Fields not included here (like password) will be excluded automatically.
    """
    name: str
    price: float
    is_offer: bool = False



# -------------------------------
# POST Endpoint using Pydantic Models
# -------------------------------
@app.post("/items/", response_model=ItemResponse)
def create_item(item: Item):
    """
    Receives an Item object in the request body, validates it automatically,
    and returns it according to the ItemResponse model.
    """
    print(item)  # Prints the received item to the console for debugging
    return item  # Only fields in ItemResponse will be returned to the client

    # Example alternative return if you want a custom message:
    # return {
    #     'message': "Item Created",
    #     'Item': item
    # }


# -------------------------------
# Notes:
# -------------------------------
# 1. FastAPI automatically generates interactive API documentation at:
#    http://127.0.0.1:8000/docs
#    Here you can test your POST request by filling out the JSON fieldsand executing it directly from your browser.
#
# 2. Automatic Validation:
#    - If you send a wrong type, e.g., price="cheap", FastAPI will return a 422 Unprocessable Entity error.
#
# 3. Response Models:
#    - By defining a separate response model (ItemResponse), you can hide sensitive fields like passwords or internal IDs from API responses.
#    - This helps keep your API responses clean and secure.

### Implements CRUD (Create, Read, Update, Delete) APIs for items
# Related files: db2.py (database), models2.py (ORM models)

from fastapi import FastAPI
from pydantic import BaseModel
from db2 import engine,SessionLocal
from models2 import Base, Item


# FastAPI app instance
app= FastAPI()

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)


# -------------------------------
# Pydantic Schema for Item
# -------------------------------
class ItemSchema(BaseModel):
    """
    Defines the data structure for incoming requests for creating/updating items.
    Attributes:
        name: Name of the item
        quantity: Number of items
        price: Price of the item
    """
    name: str
    quantity: int
    price: float



# -------------------------------
# POST Endpoint: Create Item
# -------------------------------
@app.post("/items/")
def create_item(item:ItemSchema):
    """
    Adds a new item to the database.
    Steps:
    1. Create a session
    2. Instantiate an Item ORM object
    3. Add and commit the item
    4. Refresh to get auto-generated fields (id)
    5. Close session and return item
    """
    db= SessionLocal()
    db_item= Item(name=item.name, quantity=item.quantity, price=item.price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    db.close()
    return db_item


# -------------------------------
# GET Endpoint: Read Item by ID
# -------------------------------
@app.get("/items/{item_id}")
def get_item(item_id: int):
    """
    Fetches a single item by its ID.
    Returns an error message if not found.
    """
    db= SessionLocal()
    item= db.query(Item).filter(Item.id==item_id).first()
    db.close()
    if not item:
        return {"error": "Item not found!!"}
    return item


# -------------------------------
# PUT Endpoint: Update Item
# -------------------------------
@app.put("/items/{item_id}")
def update_item(item_id: int, item: ItemSchema):
    """
    Updates an existing item.
    Steps:
    1. Query the item by ID
    2. If not found, return error
    3. Update fields
    4. Commit changes
    5. Refresh and return updated item
    """
    db=SessionLocal()
    db_item= db.query(Item).filter(Item.id==item_id).first()
    if not db_item:
        db.close()
        return {"error": "Item not found!!"}
    db_item.name= item.name
    db_item.quantity= item.quantity
    db_item.price= item.price
    db.commit()
    db.refresh(db_item)
    db.close()
    return db_item


# -------------------------------
# DELETE Endpoint: Delete Item
# -------------------------------
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """
    Deletes an item by ID.
    Returns an error message if the item is not found.
    """
    db= SessionLocal()
    db_item= db.query(Item).filter(Item.id==item_id).first()
    if not db_item:
        db.close()
        return {"error": "Item not found!!"}
    db.delete(db_item)
    db.commit()
    db.close()
    return {"message": "Item deleted sucessfully!!"}

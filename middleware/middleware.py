### Demonstrates how to implement Middleware in FastAPI

# -------------------------------
# What is Middleware?
# -------------------------------
# Middleware functions run *before* and/or *after* a request reaches the route handler.
# They can:
#   - Log requests or responses
#   - Modify request or response objects
#   - Perform authentication/authorization checks
#   - Measure performance
#   - Enforce rules or validations

from fastapi import FastAPI, Request
import time


# Create FastAPI instance
app= FastAPI()


# -------------------------------
# Custom Middleware to Log Request Time
# -------------------------------
@app.middleware("http")
async def log_request_time(request: Request, call_next):
    """
    Middleware function that logs the time taken to process each request.

    Parameters:
    - request: Incoming HTTP request
    - call_next: Function to call the next step in the request lifecycle (usually the route handler)

    Steps:
    1. Record start time
    2. Call the actual route handler with call_next(request)
    3. Measure the total processing time
    4. Print log to console
    5. Return the response
    """
    start_time= time.time() # Record time when request started
    response= await call_next(request)  # Call the actual route
    process_time= time.time()-start_time # Calculate elapsed time
    print(f"Request: {request.method} {request.url} - Process time: {process_time:.4f} seconds")
    return response


# -------------------------------
# Example Route
# -------------------------------
@app.get("/")
def read_root():
    """
    A simple GET route to test middleware.
    Visiting http://127.0.0.1:8000/ will trigger the middleware first,
    then this route, and log the request processing time.
    """
    return {"Hello": "World"}


# -------------------------------
# Notes:
# -------------------------------
# 1. Middleware is global: it affects all routes in the app.
# 2. The call_next function must always be called to continue processing the request.
# 3. You can have multiple middleware functions; they run in the order they are added.
# 4. Middleware can also modify requests/responses if needed (e.g., adding headers).

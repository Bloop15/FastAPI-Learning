### Demonstrates Jinja2 templating and HTML form submission in FastAPI
# Related files:
#   - templates/index.html   -> Input form page
#   - templates/result.html  -> Page to display results after form submission

# Install dependencies:
#   pip install jinja2 python-multipart fastapi[all]
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path


# -------------------------------
# FastAPI Instance
# -------------------------------
app= FastAPI()


# -------------------------------
# Setup Templates Directory
# -------------------------------
BASE_DIR= Path(__file__).resolve().parent
templates= Jinja2Templates(directory=BASE_DIR/"templates")


# -------------------------------
# GET Endpoint: Render Input Form
# -------------------------------
@app.get('/', response_class=HTMLResponse)
def read_root(request: Request):
    """
    Render the index.html template.
    - request: required by Jinja2Templates to include request context
    """
    return templates.TemplateResponse("index.html", {"request":request})


# -------------------------------
# POST Endpoint: Handle Form Submission
# -------------------------------
@app.post("/submit", response_class=HTMLResponse)
def submit_form(request: Request, username: str=Form(...), freq: int=Form(...)):
    """
    Receives form data and renders the result.html template.
    - username: input from text field
    - freq: input from number field
    """
    context= {
        "request": request,
        "username": username,
        "loop_freq": range(freq)
    }
    return templates.TemplateResponse("result.html", context)

 
# -------------------------------
# Jinja2 Notes
# -------------------------------
"""
- Jinja2 allows embedding Python-like expressions in HTML:
    {{ variable }}              -> Display variable value
    {% if condition %} ... {% endif %} -> Conditional statements
    {% for item in items %} ... {% endfor %} -> Loops
    {# comment #}               -> Comment in template (not rendered)

- Use Case:
    - Render HTML templates with dynamic data.
    - Keep backend logic separate from frontend HTML.
"""

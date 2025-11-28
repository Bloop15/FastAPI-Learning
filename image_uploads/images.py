# Demonstrates handling image uploads in FastAPI
# Related files:
#   - templates/form.html         -> Form to upload image
#   - templates/result_image.html -> Page to show uploaded image and info
#   - static/uploads/             -> Folder to store uploaded images

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import os


# -------------------------------
# FastAPI instance
# -------------------------------
app= FastAPI()

# Serve static files from "static" directory
# This allows access to uploaded images via /static/uploads/<filename>
app.mount("/static", StaticFiles(directory="static"), name="static")


# Setup Jinja2 templates directory
templates= Jinja2Templates(directory="templates")

# Directory to save uploaded files
UPLOAD_DIR= "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True) # Create folder if it doesn't exist


# -------------------------------
# GET Endpoint: Render Upload Form
# -------------------------------
@app.get("/", response_class=HTMLResponse)
def form_page(request: Request):
    """
    Renders form.html template with an upload form.
    """
    return templates.TemplateResponse("form.html", {"request": request})


# -------------------------------
# POST Endpoint: Handle File Upload
# -------------------------------
@app.post("/upload", response_class=HTMLResponse)
async def upload(request: Request, file: UploadFile= File(...)):
    """
    Receives an uploaded image and saves it to UPLOAD_DIR.
    - file: Uploaded image file
    Steps:
        1. Build file path
        2. Save file using shutil.copyfileobj
        3. Prepare file info dictionary (filename, type, URL)
        4. Render result_image.html with file info
    """
    file_location= os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, 'wb') as f:
        shutil.copyfileobj(file.file, f)
    
    file_info= {
        'filename': file.filename,
        'content_type': file.content_type,
        'image_url': f"/static/uploads/{file.filename}"   # URL for preview
    }

    return templates.TemplateResponse("result_image.html", {"request": request, "file_info": file_info})

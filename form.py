from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
import shutil
import os
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()
app.mount("/media", StaticFiles(directory="media"), name="media")
templates = Jinja2Templates(directory="templates")

# Set the path for storing uploaded images
UPLOAD_FOLDER = 'media'

@app.get("/")
def form(request: Request):
    return templates.TemplateResponse("imgform.html", {"request": request})

@app.post("/")
async def upload_image(request: Request, image: UploadFile = File(...)):
    # Save the file to the upload folder
    with open(os.path.join(UPLOAD_FOLDER, image.filename), "wb") as buffer:
        print(os.path.join(UPLOAD_FOLDER, image.filename))
        shutil.copyfileobj(image.file, buffer)

    return HTMLResponse(content=f"""
        <h2>Uploaded Image:</h2>
        <img src="/media/{image.filename}" alt="Uploaded Image">
    """)
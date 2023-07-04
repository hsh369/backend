from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
from starlette.requests import Request as StarletteRequest
import os
from fastapi import FastAPI, File, UploadFile
import shutil
import base64
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from img_upload import imagekit 
import imgprocessing

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")
templates = Jinja2Templates(directory="templates")

# Set the path for storing uploaded images
UPLOAD_FOLDER = 'media'

# @app.get("/items/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse("item.html", {"request": request, "id": id})



@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# @app.post("/")
# async def upload_image(request: Request, image: UploadFile = File(...)):
#     # imagekit.upload_file(
#     # file= image.file,
#     # file_name= f"{image.filename}",)
    
#     obj_list = imgprocessing.get_objects_list("https://img.freepik.com/premium-photo/red-apples-isolated-white-background_299651-65.jpg?w=2000")
    
#     detailed_items = imgprocessing.get_object_details(obj_list)

#     return templates.TemplateResponse("results.html", {"request":request,"items": detailed_items})


@app.get("/items", response_class=HTMLResponse)
def read_item(request: Request):
    url = "https://media.designcafe.com/wp-content/uploads/2023/01/31151510/contemporary-interior-design-ideas-for-your-home.jpg"
    obj_list = imgprocessing.get_objects_list(url)
    
    detailed_items = imgprocessing.get_object_details(obj_list)
    for i in detailed_items:
        item = detailed_items[i]
        image_path = imgprocessing.crop_image(url,item)
        item["image"] = image_path
    return templates.TemplateResponse("results.html", {"request": request, "items": detailed_items.items(),"url":url})
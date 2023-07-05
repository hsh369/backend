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
from img_draw import draw_borders_on_image
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
    url = "https://images.hindustantimes.com/img/2022/09/20/1600x900/office-g906b017c5_1920_1663669914946_1663669956567_1663669956567.jpg"
    obj_list = imgprocessing.get_objects_list(url)
    
    detailed_items = imgprocessing.get_object_details(obj_list)
    # for i in detailed_items:
    #     item = detailed_items[i]
    #     image_path = imgprocessing.crop_image(url,item)
    #     item["image"] = image_path
    # summary = imgprocessing.summurize(str(detailed_items))
    borders_list = []
    for item in list(detailed_items.values()):
        borders_list.append((item['x_min'],item['x_max'],item['y_min'],item['y_max']))
    img_url = draw_borders_on_image(url, borders_list)
    return templates.TemplateResponse("results.html", {"request": request, "items": detailed_items.items(),"url":url, "img_url":img_url})
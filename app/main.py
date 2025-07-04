from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from pathlib import Path
import uvicorn
import os
from utils.file_utils import is_allowed_file, get_unique_name, get_images_in_dir, MAX_FILE_SIZE

load_dotenv()

app = FastAPI()
app.mount("/statics", StaticFiles(directory="statics"), name="statics")
app.mount("/image", StaticFiles(directory="images"), name="image")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context=context)

@app.post("/")
async def upload(request: Request, file: UploadFile = File(...)):
    content = await file.read(MAX_FILE_SIZE + 1)

    if not is_allowed_file(Path(file.filename)):
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "status": "ERROR",
                "code": 406,
                "detail": "Not Acceptable",
            }
        )    
    if len(content) > MAX_FILE_SIZE:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "status": "ERROR",
                "code": 413,
                "detail": "Content Too Large",
            }
        )    
    new_filename = get_unique_name(content, Path(file.filename))
    file_url = f"{request.base_url}image/{new_filename}"

    images_dir = Path("images")
    images_dir.mkdir(exist_ok=True)
    path = images_dir/new_filename
    path.write_bytes(content)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "status": "OK",
            "filename": new_filename,
            "url": file_url
        }
    )

@app.get("/images", response_class=HTMLResponse)
async def images(request: Request, deleted = None):
    images = []
    files = get_images_in_dir("images")
    for file in files:
        url = f"{request.base_url}image/{file.name}"
        images.append({"name":file.name, "url": url})
    return templates.TemplateResponse(
        "images.html",
        {
            "request": request,
            "status": "OK",
            "images": images,
            "deleted": deleted
        }
    )

@app.post("/delete")
async def delete(request: Request, api_key: str = Form(...), image_name: str = Form(...)):
        if api_key != os.getenv('API_KEY'):
            return await images(request, False)
        else:
            images_dir = Path("images")
            path = images_dir/image_name
            if path.exists():
                path.unlink()
            return await images(request, True)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
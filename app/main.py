from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from pathlib import Path
from utils.file_utils import is_allowed_file, get_unique_name, MAX_FILE_SIZE

app = FastAPI()
app.mount("/statics", StaticFiles(directory="app/statics"), name="statics")
app.mount("/image", StaticFiles(directory="images"), name="image")
templates = Jinja2Templates(directory="app/templates")

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
    new_filename = get_unique_name(Path(file.filename))
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
async def root(request: Request):
    context = {"request": request}
    return templates.TemplateResponse(
        "images.html",
        {
            "request": request,
            "status": "OK",
            "images": [
                {
                    "name": "97b6d2fe-ef3c-4d0c-a6c6-8367e4948c78",
                    "url": "http://127.0.0.1:8000/image/97b6d2fe-ef3c-4d0c-a6c6-8367e4948c78.jpg"
                },
                {
                    "name": "d1a5effe-6720-41ac-95a0-1dc441134491",
                    "url": "http://127.0.0.1:8000/image/d1a5effe-6720-41ac-95a0-1dc441134491.jpg"
                },
                {
                    "name": "d1a5effe-6720-41ac-95a0-1dc441134491",
                    "url": "http://127.0.0.1:8000/image/d1a5effe-6720-41ac-95a0-1dc441134491.jpg"
                },
                {
                    "name": "d1a5effe-6720-41ac-95a0-1dc441134491",
                    "url": "http://127.0.0.1:8000/image/d1a5effe-6720-41ac-95a0-1dc441134491.jpg"
                },
                {
                    "name": "d1a5effe-6720-41ac-95a0-1dc441134491",
                    "url": "http://127.0.0.1:8000/image/d1a5effe-6720-41ac-95a0-1dc441134491.jpg"
                }         
            ]
        }
    )


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
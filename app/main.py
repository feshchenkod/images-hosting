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

@app.get("/images", response_class=HTMLResponse)
async def root(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("images.html", context=context)

@app.post("/upload")
async def upload(request: Request, file: UploadFile = File(...)):
    content = await file.read(MAX_FILE_SIZE + 1)

    if not is_allowed_file(Path(file.filename)):
        raise HTTPException(status_code=406, detail="Not Acceptable")
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="Content Too Large")
    
    new_filename = get_unique_name(Path(file.filename))

    images_dir = Path("images")
    images_dir.mkdir(exist_ok=True)
    path = images_dir/new_filename
    path.write_bytes(content)

    return {"status": "OK", "filename": f"{new_filename}", "url": f"{request.base_url}image/{new_filename}"}

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
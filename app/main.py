import os
import math
import uvicorn
from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
from pathlib import Path
from utils.file_utils import is_allowed_file, get_unique_name, get_images_in_dir, MAX_FILE_SIZE
from utils.db_utils import get_conn

load_dotenv()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.getenv('SESSION_SECRET_KEY'))
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
    file_path = Path(file.filename)

    if not is_allowed_file(file_path):
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
    new_filename = get_unique_name(content, file_path)
    file_url = f"{request.base_url}image/{new_filename}"

    images_dir = Path("images")
    images_dir.mkdir(exist_ok=True)
    path = images_dir/new_filename
    path.write_bytes(content)

    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO images(
	            filename, original_name, size, file_type)
	        VALUES (%s, %s, %s, %s);
            """, (path.stem, file_path.stem, path.stat().st_size, path.suffix)
        )
        conn.commit()

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
async def images(request: Request, current_page: int = Query(default=1, alias="page")):
    deleted = request.session.pop("deleted", None)
    conn = get_conn()
    offset = (current_page - 1) * 5

    with conn.cursor() as cur:
        length = cur.execute("SELECT count(*) FROM images").fetchone()[0]
        cur.execute("SELECT * FROM images ORDER BY upload_time DESC LIMIT 5 OFFSET %s", (offset,))
        result = cur.fetchall()
    
    total_pages = math.ceil(length / 5)

    return templates.TemplateResponse(
        "images.html",
        {
            "request": request,
            "status": "OK",
            "images": result,
            "deleted": deleted,
            "total_pages": total_pages,
            "current_page": current_page
        }
    )

@app.post("/delete")
async def delete(request: Request, api_key: str = Form(...), image_id: int = Form(...)):
        if api_key != os.getenv('API_KEY'):
            request.session["deleted"] = False
            return RedirectResponse(url=f"/images", status_code=303)
        else:
            conn = get_conn()
            with conn.cursor() as cur:

                image_name = ''.join(cur.execute("""
                    SELECT filename, file_type
                    FROM images
                    WHERE id = %s;
                    """, (image_id,)
                ).fetchone())

                cur.execute("""
                    DELETE FROM images
                    WHERE id = %s;
                    """, (image_id,)
                )
                conn.commit()

                image_count = cur.execute("""
                    SELECT count(*)
                    FROM images
                    WHERE filename = %s;
                    """, (image_name.split('.')[0],)
                ).fetchone()[0]

            if not image_count:
                images_dir = Path("images")
                path = images_dir/image_name
                if path.exists():
                    path.unlink()
            request.session["deleted"] = True
            return RedirectResponse(url=f"/images", status_code=303)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
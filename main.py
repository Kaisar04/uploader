from fastapi import FastAPI, UploadFile, File, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from service import upload_file

import io
import time
import os
import psutil

app = FastAPI()

templates = Jinja2Templates(directory='templates')


async def get_memory():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss


@app.get("/", response_class=HTMLResponse)
async def get_page(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


@app.post("/upload")
async def upload(
        file: UploadFile = File(...)
):
    before = await get_memory()
    tic = time.perf_counter()
    await upload_file(file)
    toc = time.perf_counter()

    after = await get_memory()
    print(f"Uploaded in {toc - tic:0.4f} seconds")
    print((after - before) / 1024 ** 2, 'MB')
    return Response(status_code=200, content="Successfully uploaded")

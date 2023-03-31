from fastapi import FastAPI, UploadFile, File, Request, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

import asyncio
import boto3
import os


load_dotenv()

access_key = os.getenv('ACCESS_KEY')
secret_access_key = os.getenv('SECRET_ACCESS_KEY')
bucket_name = os.getenv('BUCKET_NAME')

GB = 1024 ** 3
MB = 1024 ** 2


app = FastAPI()

templates = Jinja2Templates(directory='templates')


async def read_chunk(file):
    while True:
        data = await file.read(10 * MB)
        if not data:
            break
        yield data


def get(index, chunk):
    print(len(chunk), index)
    return index


async def call_comp(loop, index, chunk):
    print('called an executor')
    r = None
    r = await loop.run_in_executor(None, get, index, chunk)
    return r


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
    tasks = []
    loop = asyncio.get_event_loop()
    index = 0
    async for chunk in read_chunk(file):
        index += 1
        tasks.append(asyncio.create_task(
            call_comp(loop, index, chunk)
        ))
    results = await asyncio.gather(*tasks)
    return results



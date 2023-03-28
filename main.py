from fastapi import FastAPI, UploadFile, File, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from credentials import access_key, secret_access_key
import boto3
from boto3.s3.transfer import TransferConfig
import io
import time
import os
import psutil

bucket_name = 'qaisarymsaq-files'

app = FastAPI()

templates = Jinja2Templates(directory='templates')

GB = 1024 ** 3
MB = 1024 ** 2

# session = boto3.session.Session()


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

    config = TransferConfig(multipart_threshold=400*MB,
                            max_concurrency=10,
                            multipart_chunksize=50*MB,
                            use_threads=True)
    client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)
    client.upload_fileobj(file.file, bucket_name, file.filename, Config=config)
    after = await get_memory()
    print((after - before) / 1024 ** 2, 'MB')

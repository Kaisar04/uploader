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


def upload_file(client, multipart, index, chunk):
    response = client.upload_part(
        Body=chunk,
        Bucket=bucket_name,
        Key='largeobject',
        PartNumber=index,
        UploadId=multipart['UploadId'],
    )

    return response


async def call_comp(loop, client, response, index, chunk):
    print('called an executor')
    r = None
    r = await loop.run_in_executor(None, upload_file, client, response, index, chunk)
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
    session = boto3.session.Session()
    client = session.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)
    response = client.create_multipart_upload(
        Bucket=bucket_name,
        Key='largeobject',
    )

    tasks = []
    loop = asyncio.get_event_loop()
    index = 0
    async for chunk in read_chunk(file):
        index += 1
        tasks.append(asyncio.create_task(
            call_comp(loop, client, response, index, chunk)
        ))
    results = await asyncio.gather(*tasks)

    part_info = {
        'Parts': [
            {
                'PartNumber': 1,
                'ETag': part['ETag']
            }
        ]
    }

    complete = client.complete_multipart_upload(Bucket=bucket_name, Key='largeobject', UploadId=mpu['UploadId'],
                                 MultipartUpload=part_info)

    return complete



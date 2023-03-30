import boto3
from boto3.s3.transfer import TransferConfig
import os
from dotenv import load_dotenv
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

access_key = os.getenv('ACCESS_KEY')
secret_access_key = os.getenv('SECRET_ACCESS_KEY')
bucket_name = os.getenv('BUCKET_NAME')

GB = 1024 ** 3
MB = 1024 ** 2


async def upload_file(client, response, file):
    response = client.upload_part(
        Body=file,
        Bucket=bucket_name,
        Key='largeobject',
        PartNumber='1',
        UploadId=response['UploadId'],
    )

    return response


async def parallel_multithreading_upload(file):
    session = boto3.session.Session()
    client = session.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)
    response = client.create_multipart_upload(
        Bucket=bucket_name,
        Key='largeobject',
    )

    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_key = {executor.submit(upload_file, client, response, key): key for key in file}

        for future in futures.as_completed(future_to_key):
            key = future_to_key[future]
            exception = future.exception()

            if not exception:
                yield key, future.result()
            else:
                yield key, exception





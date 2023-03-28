from credentials import access_key, secret_access_key
import boto3
from boto3.s3.transfer import TransferConfig


session = boto3.session.Session()


bucket_name = 'qaisarymsaq-files'
GB = 1024 ** 3
MB = 1024 ** 2


async def upload_file(file):
    config = TransferConfig(multipart_threshold=400 * MB,
                            max_concurrency=10,
                            multipart_chunksize=50 * MB,
                            use_threads=True)
    client = session.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)
    client.upload_fileobj(file.file, bucket_name, file.filename, Config=config)


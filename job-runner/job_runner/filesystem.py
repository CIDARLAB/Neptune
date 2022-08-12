import uuid
import boto3
from pprint import pprint
from pathlib import Path

from job_runner.setting import AWS_ENDPOINT_URL, AWS_S3_BUCKET_NAME

S3_CLIENT = boto3.client(
        "s3",
        endpoint_url=AWS_ENDPOINT_URL
    )

def upload_file_using_client(file_location: Path):
    """
    Uploads file to S3 bucket using S3 client object
    :return: None
    """
    bucket_name = AWS_S3_BUCKET_NAME
    file_name = file_location.name
    file_path = str(file_location.absolute())
    s3_object_name = f"{str(uuid.uuid4())}-{file_name}"
    S3_CLIENT.upload_file(file_path, bucket_name, s3_object_name)
    
    print(f"Uploaded {file_path} to {bucket_name}/{file_name}")
    
from typing import List
import uuid
import boto3
from pprint import pprint
from pathlib import Path

from job_runner.setting import AWS_ENDPOINT_URL, AWS_S3_BUCKET_NAME

S3_CLIENT = boto3.client(
        "s3",
        endpoint_url=AWS_ENDPOINT_URL
    )

def upload_file_using_client(file_location: Path) -> str:
    """ Uploads file to S3 bucket using S3 client object

    Args:
        file_location (Path): Location of the file to upload

    Returns:
        str: S3 object name  
    """
    bucket_name = AWS_S3_BUCKET_NAME
    file_name = file_location.name
    file_path = str(file_location.absolute())
    s3_object_name = f"{str(uuid.uuid4())}-{file_name}"
    S3_CLIENT.upload_file(file_path, bucket_name, s3_object_name)
    
    print(f"Uploaded {file_path} to {bucket_name}/{file_name}")
    
    return s3_object_name

def download_file_using_client(s3_object_name: str, local_file_name: str, download_directory: Path) -> None:
    """ Downloads file from S3 bucket using S3 client object

    Args:
        s3_object_name (str): name of the S3 object to download
        local_file_name (str): name of the local file to download to
        download_directory (Path): location of the file to download

    Returns:
        None: None
    """
    local_file_path_location = str(download_directory.joinpath(local_file_name).absolute())
    S3_CLIENT.download_file(AWS_S3_BUCKET_NAME, s3_object_name, local_file_path_location)
    
    print(f"Downloaded {s3_object_name} from {AWS_S3_BUCKET_NAME} to {local_file_path_location}")
        
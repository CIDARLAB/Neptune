import boto3
from pprint import pprint
from pathlib import Path

from job_runner.setting import AWS_ENDPOINT_URL, AWS_S3_BUCKET_NAME



def upload_file_using_client(file_location: Path):
    """
    Uploads file to S3 bucket using S3 client object
    :return: None
    """
    s3 = boto3.client(
        "s3",
        endpoint_url=AWS_ENDPOINT_URL
    )
    bucket_name = AWS_S3_BUCKET_NAME
    object_name = file_location.name
    file_path = file_location.absolute()

    response = s3.upload_file(file_path, bucket_name, object_name)
    pprint(response)  # prints None

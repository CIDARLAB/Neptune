import os
import uuid
import boto3
from pathlib import Path

from app.parameters import AWS_ACCESS_KEY_ID, AWS_ENDPOINT_URL, AWS_S3_BUCKET_NAME, AWS_SECRET_ACCESS_KEY



S3_CLIENT = boto3.client(
    "s3",
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    endpoint_url=AWS_ENDPOINT_URL,
    
)
class FileSystem:
    
    @staticmethod
    def upload_file(file_location: Path) -> str:
        """ Uploads file to S3 bucket using S3 client object

        Args:
            file_location (Path): Location of the file to upload
        """
        bucket_name = AWS_S3_BUCKET_NAME
        file_name = file_location.name
        file_path = str(file_location.absolute())
        s3_object_name = f"{str(uuid.uuid4())}-{file_name}"
        S3_CLIENT.upload_file(file_path, bucket_name, s3_object_name)
        
        print(f"Uploaded {file_path} to {bucket_name}/{s3_object_name}")
        
        return s3_object_name
    
    @staticmethod
    def download_file(s3_location:str, download_location: Path) -> None:
        """Downloads the file from the S3 bucket to the file system

        Args:
            s3_location (str): The location of the file in the S3 bucket
            download_location (Path): The directory location to download the file
        """
        # Find cleaned name by removing uuid from s3_location
        file_name = s3_location.split('-')[-1]
        full_file_path = download_location.joinpath(file_name)
        S3_CLIENT.download_file(AWS_S3_BUCKET_NAME, s3_location, str(full_file_path.absolute()))
        
        print(f"Downloaded {s3_location} from {AWS_S3_BUCKET_NAME} to {download_location.absolute()}")
        
    @staticmethod
    def delete_file(s3_location:str) -> None:
        """Deletes the file from the s3 bucket

        Args:
            s3_location (str): The location of the file in the S3 bucket
        """
        S3_CLIENT.delete_object(Bucket=AWS_S3_BUCKET_NAME, Key=s3_location)
        
        print(f"Deleted {s3_location} from {AWS_S3_BUCKET_NAME}")

    @staticmethod
    def copy_file(s3_location:str) -> str:
        """ Makes a copy of the file in the s3 bucket

        It generates a new UUID and preserves the same name

        Args:
            s3_location (str): The location of the file in the S3 bucket
        """
        file_name = s3_location.split('-')[-1]
        new_s3_location = f"{str(uuid.uuid4())}-{file_name}"
        S3_CLIENT.copy_object(Bucket=AWS_S3_BUCKET_NAME, Key=new_s3_location, CopySource=f"{AWS_S3_BUCKET_NAME}/{s3_location}")
        
        print(f"Copied {s3_location} from {AWS_S3_BUCKET_NAME} to {new_s3_location}")
        
        return new_s3_location
        
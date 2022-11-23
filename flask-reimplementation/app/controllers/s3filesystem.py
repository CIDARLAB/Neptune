import os
from typing import Optional
import uuid
import boto3
from pathlib import Path
from botocore.exceptions import ClientError

from app.parameters import AWS_ACCESS_KEY_ID, AWS_ENDPOINT_URL, AWS_S3_BUCKET_NAME, AWS_SECRET_ACCESS_KEY



S3_CLIENT = boto3.client(
    "s3",
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    endpoint_url=AWS_ENDPOINT_URL,
    
)

class S3FileSystem:
    """Class to handle the virtual file system enabled by S3

    It has the methods for uploading, downloading, deleteing and copying files

    """

    @staticmethod
    def test_connection() -> bool:
        """Test the connection to the S3 bucket

        Returns:
            bool: True if the connection is successful, False otherwise
        """
        try:
            S3_CLIENT.head_bucket(Bucket=AWS_S3_BUCKET_NAME)
            return True
        except ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 403:
                print(f"Private Bucket {AWS_S3_BUCKET_NAME}. Forbidden Access! ")
            elif error_code == 404:
                print(f"Bucket {AWS_S3_BUCKET_NAME}. Does Not Exist!")            
            return False


    @staticmethod
    def genenerate_s3_file_name(file_name: str) -> str:
        """Generate a unique file key for the S3 bucket

        Args:
            file_name (str): The name of the file

        Returns:
            str: The unique file key
        """
        return f"{uuid.uuid4()}-{file_name}"


    @staticmethod
    def decode_s3_file_name(s3_file_key: str) -> str:
        """Decode the file name from the S3 file key

        Args:
            s3_file_key (str): The S3 file key

        Returns:
            str: The file name
        """
        return s3_file_key.split("-")[-1]


    @staticmethod
    def create_new_file(file_name: str) -> str:
        """Create a new file in the S3 bucket

        Args:
            file_name (str): The name of the file to create
            file_content (str): The content of the file to create

        Returns:
            bool: True if the file was created successfully, False otherwise
        """
        s3_location = S3FileSystem.genenerate_s3_file_name(file_name)
        try:
            S3_CLIENT.put_object(
                Bucket=AWS_S3_BUCKET_NAME,
                Key=s3_location,
            )
            return s3_location
        except ClientError as e:
            print(f"Error creating file: {e}")
            return ""
    
    @staticmethod
    def update_file_content(s3_location: str, file_content: str = "") -> bool:
        """Updates the file in the S3 bucket

        Args:
            file_name (str): The name of the file to create
            file_content (str): The content of the file to create

        Returns:
            bool: True if the file was created successfully, False otherwise
        """
        try:
            S3_CLIENT.put_object(
                Bucket=AWS_S3_BUCKET_NAME,
                Key=s3_location,
                Body=file_content
            )
            return True
        except ClientError as e:
            print(f"Error creating file: {e}")
            return False

    @staticmethod
    def upload_file(file_location: Path, override_file_name="") -> str:
        """ Uploads file to S3 bucket using S3 client object

        This fuction also provides the ability to have an overriden file name that needs to be passed in
        the case of uploading uploaded files to the S3 bucket. This way we can ensure that the uploaded
        files dont have a randomly generated name.

        Args:
            file_location (Path): Location of the file to upload
            override_file_name (str): The name of the file to override the file name with
        """
        file_name = file_location.name
        
        if override_file_name:
            file_name = override_file_name

        file_path = str(file_location.absolute())
        s3_object_name = S3FileSystem.genenerate_s3_file_name(file_name)
        S3_CLIENT.upload_file(file_path, AWS_S3_BUCKET_NAME, s3_object_name)
        
        print(f"Uploaded {file_path} to {AWS_S3_BUCKET_NAME}/{s3_object_name}")
        
        return s3_object_name
    
    @staticmethod
    def download_file(s3_location:str, download_location: Path, preserve_s3_name: bool= False) -> None:
        """Downloads the file from the S3 bucket to the file system

        Args:
            s3_location (str): The location of the file in the S3 bucket
            download_location (Path): The directory location to download the file
            preserve_s3_name (bool, optional): If True, the file will be downloaded with the s3 random name. Defaults to False.
        """
        # Find cleaned name by removing uuid from s3_location
        if preserve_s3_name:
            file_name = s3_location
        else:
            file_name = S3FileSystem.decode_s3_file_name(s3_location)
        
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
        new_s3_location = S3FileSystem.genenerate_s3_file_name(file_name)
        S3_CLIENT.copy_object(Bucket=AWS_S3_BUCKET_NAME, Key=new_s3_location, CopySource=f"{AWS_S3_BUCKET_NAME}/{s3_location}")
        
        print(f"Copied {s3_location} from {AWS_S3_BUCKET_NAME} to {new_s3_location}")
        
        return new_s3_location

    @staticmethod 
    def overwrite_file(s3_location:str, file_location: Path) -> None:
        """Updates the file in the s3 bucket

        Args:
            s3_location (str): The location of the file in the S3 bucket
            file_location (Path): The location of the file in the file system
        """
        S3FileSystem.delete_file(s3_location)
        S3_CLIENT.upload_file(file_location, AWS_S3_BUCKET_NAME, s3_location)
        
        print(f"Updated {s3_location} from {AWS_S3_BUCKET_NAME} with payload")
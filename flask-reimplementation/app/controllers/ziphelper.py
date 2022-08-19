from pathlib import Path
from typing import List
import uuid
from zipfile import ZipFile
from app.controllers.filesystem import S3_CLIENT

from app.parameters import AWS_S3_BUCKET_NAME


def download_files_and_zip(s3_objects_list: List[str], download_directory: Path) -> Path:
    """ Downloads files from S3 bucket and zips them
    Args:
        s3_objects_list (List[str]): List of S3 objects to download
        download_directory (Path): Directory to download the files to
    Returns:
        Path: Path to the zip file
    """
    zip_file_name = f"{str(uuid.uuid4())}.zip"
    zip_file_path = download_directory.joinpath(zip_file_name)
    with ZipFile(zip_file_path, 'w') as zip_file:
        for s3_object in s3_objects_list:
            file_name = s3_object.split('-')[-1]
            local_file_path = download_directory.joinpath(file_name)
            S3_CLIENT.download_file(AWS_S3_BUCKET_NAME, s3_object, str(local_file_path.absolute()))
            zip_file.write(local_file_path, file_name)
            local_file_path.unlink()
    
    return zip_file_path
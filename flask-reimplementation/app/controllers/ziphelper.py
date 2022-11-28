from pathlib import Path
from typing import List
import uuid
from zipfile import ZipFile
from app.controllers.s3filesystem import S3_CLIENT, S3FileSystem

from app.parameters import AWS_S3_BUCKET_NAME, FLASK_DOWNLOADS_DIRECTORY


def download_s3files_and_zip(s3_objects_list: List[str]) -> Path:
    """ Downloads files from S3 bucket and zips them
    Args:
        s3_objects_list (List[str]): List of S3 objects to download
        download_directory (Path): Directory to download the files to
    Returns:
        Path: Path to the zip file
    """
    zip_file_name = f"{str(uuid.uuid4())}.zip"
    zip_file_path = Path(FLASK_DOWNLOADS_DIRECTORY).joinpath(zip_file_name)
    with ZipFile(str(zip_file_path), 'w') as zip_file:
        for s3_object in s3_objects_list:
            file_name = S3FileSystem.download_file(s3_object, zip_file_path)
            zip_file.write(file_name)
            file_name.unlink()
    
    return zip_file_path
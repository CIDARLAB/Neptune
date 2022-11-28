from pathlib import Path
from typing import List
import uuid
from zipfile import ZipFile
from app.controllers.s3filesystem import S3_CLIENT, S3FileSystem
import shutil

from app.parameters import AWS_S3_BUCKET_NAME, FLASK_DOWNLOADS_DIRECTORY


def download_s3files_and_zip(s3_objects_list: List[str]) -> Path:
    """ Downloads files from S3 bucket and zips them
    Args:
        s3_objects_list (List[str]): List of S3 objects to download
        download_directory (Path): Directory to download the files to
    Returns:
        Path: Path to the zip file
    """
    zip_folder_name = str(uuid.uuid4())
    download_directory = Path(FLASK_DOWNLOADS_DIRECTORY).joinpath(zip_folder_name)
    zip_file_name = f"{zip_folder_name}.zip"
    zip_file_path = Path(FLASK_DOWNLOADS_DIRECTORY).joinpath(zip_file_name)
    try:
        download_directory.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print("Error creating directory:", e)
        return None
    with ZipFile(str(zip_file_path), 'w') as zip_file:
        for s3_object in s3_objects_list:
            file_name = S3FileSystem.download_file(s3_object, download_directory)
            zip_file.write(file_name, arcname=file_name.name)
            file_name.unlink()
    
    shutil.rmtree(download_directory)
    return zip_file_path
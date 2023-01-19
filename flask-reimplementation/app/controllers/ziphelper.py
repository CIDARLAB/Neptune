from pathlib import Path
from typing import List, Optional
import uuid
from app.models.file import File
from zipfile import ZipFile
from app.controllers.s3filesystem import S3FileSystem
import shutil

from app.parameters import FLASK_DOWNLOADS_DIRECTORY


def download_s3files_and_zip(file_object_list: List[File]) -> Optional[Path]:
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
        for file_object in file_object_list:
            s3_path = file_object.s3_path
            download_file_path = S3FileSystem.download_file(s3_path, download_directory)
            zip_file.write(download_file_path, arcname=download_file_path.name)
            download_file_path.unlink()
    
    shutil.rmtree(download_directory)
    return zip_file_path
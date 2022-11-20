from pathlib import Path
import zipfile


def zip_dir(dir: Path, filename: Path) -> None:
    """Zip the provided directory without navigating to that directory using `pathlib` module

    Args:
        dir (Path): The directory to zip
        filename (Path): The filename to save the zip file as
    """
    # Convert to Path object
    dir = Path(dir)

    with zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for entry in dir.rglob("*"):
            zip_file.write(entry, entry.relative_to(dir))

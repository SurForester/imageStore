import os
from dotenv import load_dotenv
from pathlib import Path
import uuid


load_dotenv()
MAX_FILE_SIZE = os.getenv("MAX_FILE_SIZE")
FILE_EXTENSIONS = os.getenv("FILE_EXTENSIONS")
files_list = []


async def check_extensions(file: Path) -> bool:
    ext = file.suffix.lower()
    return ext in FILE_EXTENSIONS


async def check_size(size: int) -> bool:
    return size <= int(MAX_FILE_SIZE)


async def get_unique_name(file: Path) -> str:
    return f"{uuid.uuid4().hex}###{file.name}"


async def delete_file(file: Path):
    file.unlink()
    return


async def get_files_list():
    file_list = []
    image_dir = Path("images")
    image_dir.mkdir(exist_ok=True)
    dirpath = Path(image_dir)
    files_list = [f for f in dirpath.iterdir() if f.is_file()]
    for x in dirpath.iterdir():
        if x.is_file():
            names = x.name.split("###")
            record = {"name": names[1], "filename": x.name}
            file_list.append(record)
    return file_list

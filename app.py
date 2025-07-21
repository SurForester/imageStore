from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from pathlib import Path
import logging
from datetime import datetime
from tools.files_tools import check_extensions, check_size, get_unique_name, get_files_list, MAX_FILE_SIZE, files_list


log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "app.log"

logging.basicConfig(
    level=logging.INFO,
    format="[{asctime}] - {levelname}: {message}",
    style="{",
    handlers=[
        logging.FileHandler(log_file, mode="a", encoding="utf-8"),
        logging.StreamHandler(),
    ]
)

class WrongFileExtention(Exception):
    pass

class WrongFileSize(Exception):
    pass

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get('/', response_class=HTMLResponse)
async def root_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/upload', response_class=HTMLResponse)
async def upload_templ(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/upload/")
async def load_img(request: Request, file: UploadFile = File(...)):
    try:
        logging.info(f'Получен файл - {file.filename}')
        image_dir = Path("images")
        image_dir.mkdir(exist_ok=True)
        inp_file = Path(file.filename)
        if not check_extensions(inp_file):
            raise WrongFileExtention
        content = await file.read(MAX_FILE_SIZE)
        if not check_size(len(content)):
            raise WrongFileSize
        unique_name = get_unique_name(inp_file)
        file_name = image_dir / str(unique_name)
        file_name.write_bytes(content)
        logging.info(f'Файл успешно записан ({file_name})')
    except WrongFileExtention:
        logging.error(f'У файла {file.filename} неверное расширение.')
        return templates.TemplateResponse("upload_error.html", {"request": request})
    except WrongFileSize:
        logging.error(f'Размер файла {file.filename} превышает установленнное ограничение.')
        return templates.TemplateResponse("upload_error.html", {"request": request})
    except Exception as e:
        logging.error(f'Ошибка при записи файла {file.filename}: {e}')
        return templates.TemplateResponse("upload_error.html", {"request": request})
    finally:
        return templates.TemplateResponse("upload_success.html", {"request": request})


@app.get('/images', response_class=HTMLResponse)
async def images_templ(request: Request):
    files_list = get_files_list()
    return templates.TemplateResponse("images.html", {"request": request, "files_list": files_list})


if __name__ == "__main__":
    logging.info("App starting")
    uvicorn.run("app:app", host="127.0.0.1", port=8000)
    logging.info("Image server started.")
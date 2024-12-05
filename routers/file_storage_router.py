from http import HTTPStatus
import os
from fastapi import APIRouter, Response, UploadFile
from fastapi.responses import FileResponse

file_storage_router = APIRouter()

STORAGE_DIR = "storage"

@file_storage_router.post("/")
async def upload_file(file: UploadFile):
    if file.filename is None:
        return Response(
            status_code=HTTPStatus.BAD_REQUEST, 
            content={"reason": "no filename"}
        )

    filepath = os.path.join(STORAGE_DIR, file.filename)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Write the uploaded file to the specified location
    with open(filepath, "wb") as buffer:
        while contents := await file.read(1024):  # Read the file in chunks
            buffer.write(contents)
    
    return {"filename": file.filename}

@file_storage_router.get("/all")
async def list_all_files():
    files = os.listdir(STORAGE_DIR)
    return {"files": files}


@file_storage_router.get("/{filename}")
async def download_file(filename: str):
    if filename in os.listdir(STORAGE_DIR):
        filepath = os.path.join(STORAGE_DIR, filename)
        return FileResponse(
            filepath,
            filename=filename,
            media_type='application/octet-stream'
        )

    return Response(
        status_code=HTTPStatus.NOT_FOUND, 
        content={"reason": "no file found with this filename"}
    )
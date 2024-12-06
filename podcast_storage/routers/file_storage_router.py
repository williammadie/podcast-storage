from http import HTTPStatus
import os
from fastapi import APIRouter, HTTPException, Response, UploadFile
from fastapi.responses import FileResponse

file_storage_router = APIRouter()

# 1 GB in bytes
MAX_FILE_SIZE = 1 * 1024 * 1024 * 1024
MAX_FILES_IN_STORAGE = 10


@file_storage_router.post("/")
async def upload_file(file: UploadFile):

    if file.size is None or file.filename is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail={"reason": "bad file detected"}
        )

    if file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail={"reason": "file size exceeds 1 GB"}
        )

    if file.filename is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail={"reason": "no filename"}
        )

    if len(os.listdir(os.getenv("STORAGE_DIR"))) >= MAX_FILES_IN_STORAGE:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="too many files in storage"
        )

    filepath = os.path.join(os.getenv("STORAGE_DIR"), file.filename)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Write the uploaded file to the specified location
    with open(filepath, "wb") as buffer:
        while contents := await file.read(1024):  # Read the file in chunks
            buffer.write(contents)

    return {"filename": file.filename, "size": file.size}


@file_storage_router.get("/all")
async def list_all_files():
    files = os.listdir(os.getenv("STORAGE_DIR"))
    return {"files": files}


@file_storage_router.get("/{filename}")
async def download_file(filename: str):
    if filename in os.listdir(os.getenv("STORAGE_DIR")):
        filepath = os.path.join(os.getenv("STORAGE_DIR"), filename)
        return FileResponse(
            filepath,
            filename=filename,
            media_type='application/octet-stream'
        )

    return Response(
        status_code=HTTPStatus.NOT_FOUND,
        content={"reason": "no file found with this filename"}
    )

from http import HTTPStatus
import os
from fastapi import APIRouter, Header, Response


file_streaming_router = APIRouter()

STORAGE_DIR = "storage"
CHUNK_SIZE = 1024 * 10


@file_streaming_router.get("/{filename}")
async def stream_media(filename: str, range: str = Header(None)):
    media_range = range
    if filename not in os.listdir(STORAGE_DIR):
        return HTTP(
            status_code=HTTPStatus.NOT_FOUND,
            content={"reason": "no file found with this filename"}
        )

    filepath = os.path.join(STORAGE_DIR, filename)
    start, end = media_range.replace("bytes=", "").split("-")
    start = int(start)
    end = int(end) if end else start + CHUNK_SIZE

    # Determine media type based on file extension
    if filepath.endswith((".mp3", ".m4a")):
        media_type = "audio/mpeg"
    elif filepath.endswith((".mov", ".avi", ".mp4")):
        media_type = "video/mp4"
    else:
        return Response(
            status_code=HTTPStatus.BAD_REQUEST,
            content={"reason": "unsupported file type"}
        )

    with open(filepath, "rb") as media:
        media.seek(start)
        data = media.read(end - start)
        filesize = str(os.stat(filepath).st_size)
        headers = {
            'Content-Range': f'bytes {str(start)}-{str(end)}/{filesize}',
            'Accept-Ranges': 'bytes'
        }
        return Response(
            data,
            status_code=HTTPStatus.PARTIAL_CONTENT,
            headers=headers,
            media_type=media_type
        )

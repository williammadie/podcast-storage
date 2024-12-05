from typing import Union

from fastapi import FastAPI

from routers.file_storage_router import file_storage_router
from routers.file_streaming_router import file_streaming_router

app = FastAPI()

app.include_router(file_storage_router, prefix="/file_storage", tags=["file_storage"])
app.include_router(file_streaming_router, prefix="/file_streaming", tags=["file_streaming"])

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
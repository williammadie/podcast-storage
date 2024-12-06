from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from podcast_storage.routers.file_storage_router import file_storage_router
from podcast_storage.routers.file_streaming_router import file_streaming_router

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=[
        'Content-Type',
        'Authorization',
        'cache-control',
        'expires'
        ]
)


app.include_router(file_storage_router,
                   prefix="/file_storage", tags=["file_storage"])
app.include_router(file_streaming_router,
                   prefix="/file_streaming", tags=["file_streaming"])


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/health")
def healthcheck():
    return {"status": "up"}

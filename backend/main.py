from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import SongRequest, BulkSongRequest
from queue_manager import QueueManager
from worker import DownloadWorker
from search import search_song
from downloader import download_song


queue = QueueManager()
worker = DownloadWorker(queue)


@asynccontextmanager
async def lifespan(app: FastAPI):
    worker.start()
    yield
    worker.stop()


app = FastAPI(title="YT Music Downloader", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "status": "running",
        "service": "YT Music Downloader API"
    }


@app.post("/download")
def download(request: SongRequest):
    video = search_song(request.song)
    title = video.get("title") or request.song
    download_song(video["url"], filename=title)

    return {
        "success": True,
        "title": title
    }


@app.post("/download-all")
def download_all(request: BulkSongRequest):
    added_count = 0
    for song in request.songs:
        clean_song = song.strip()
        if clean_song:
            queue.add_song(clean_song)
            added_count += 1

    return {
        "success": True,
        "message": f"{added_count} song(s) added to the queue."
    }


@app.get("/queue")
def get_queue():
    return queue.get_queue()


@app.post("/queue/clear")
def clear_queue():
    queue.clear_queue()
    return {
        "success": True
    }



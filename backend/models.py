from pydantic import BaseModel


class SongRequest(BaseModel):
    song: str


class BulkSongRequest(BaseModel):
    songs: list[str]


class QueueItem:

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.status = "waiting"
        self.title = None
        self.artist = None
        self.filename = None
        self.error = None

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "title": self.title,
            "artist": self.artist,
            "filename": self.filename,
            "error": self.error
        }
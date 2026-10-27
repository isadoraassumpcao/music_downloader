import threading
from models import QueueItem


class QueueManager:

    def __init__(self):
        self.queue = []
        self.next_id = 1
        self.lock = threading.Lock()

    # -------------------------
    # Add a new song
    # -------------------------
    def add_song(self, song_name):
        with self.lock:
            song = QueueItem(
                self.next_id,
                song_name
            )
            self.queue.append(song)
            self.next_id += 1
            return song

    # -------------------------
    # Return every song
    # -------------------------
    def get_queue(self):
        with self.lock:
            return [
                song.to_dict()
                for song in self.queue
            ]

    # -------------------------
    # First waiting song
    # -------------------------
    def get_next_song(self):
        with self.lock:
            for song in self.queue:
                if song.status == "waiting":
                    return song
            return None

    # -------------------------
    # Change status
    # -------------------------
    def update_status(self, song_id, status):
        with self.lock:
            song = self._find_song_unlocked(song_id)
            if song:
                song.status = status

    # -------------------------
    # Save YouTube title
    # -------------------------
    def update_title(self, song_id, title):
        with self.lock:
            song = self._find_song_unlocked(song_id)
            if song:
                song.title = title

    # -------------------------
    # Save artist
    # -------------------------
    def update_artist(self, song_id, artist):
        with self.lock:
            song = self._find_song_unlocked(song_id)
            if song:
                song.artist = artist

    # -------------------------
    # Save filename
    # -------------------------
    def update_filename(self, song_id, filename):
        with self.lock:
            song = self._find_song_unlocked(song_id)
            if song:
                song.filename = filename

    # -------------------------
    # Save error
    # -------------------------
    def update_error(self, song_id, error):
        with self.lock:
            song = self._find_song_unlocked(song_id)
            if song:
                song.error = error

    # -------------------------
    # Finished
    # -------------------------
    def mark_finished(self, song_id):
        self.update_status(song_id, "finished")

    # -------------------------
    # Failed
    # -------------------------
    def mark_failed(self, song_id, error):
        with self.lock:
            song = self._find_song_unlocked(song_id)
            if song:
                song.status = "failed"
                song.error = error

    # -------------------------
    # Remove completed songs
    # -------------------------
    def clear_finished(self):
        with self.lock:
            self.queue = [
                song for song in self.queue
                if song.status != "finished"
            ]

    # -------------------------
    # Find a song by ID
    # -------------------------
    def _find_song_unlocked(self, song_id):
        for song in self.queue:
            if song.id == song_id:
                return song
        return None

    def find_song(self, song_id):
        with self.lock:
            return self._find_song_unlocked(song_id)
    
    def clear_queue(self):
        with self.lock:
            self.queue.clear()
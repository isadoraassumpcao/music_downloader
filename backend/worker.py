import threading
import time
import re
from search import search_song
from downloader import download_song, sanitize_filename


class DownloadWorker:

    def __init__(self, queue):
        self.queue = queue
        self.running = False
        self.thread = None

    def start(self):
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(
            target=self.run,
            daemon=True
        )
        self.thread.start()
        print("Download Worker started.")

    def stop(self):
        self.running = False
        print("Download Worker stopped.")

    def run(self):
        while self.running:
            song = self.queue.get_next_song()

            if song is None:
                time.sleep(1)
                continue

            try:
                self.queue.update_status(
                    song.id,
                    "searching"
                )

                print(f"Searching: {song.name}")

                video = search_song(song.name)

                self.queue.update_title(
                    song.id,
                    video["title"]
                )

                self.queue.update_artist(
                    song.id,
                    video["artist"]
                )

                self.queue.update_status(
                    song.id,
                    "downloading"
                )

                print(f"Downloading: {video['title']}")

                artist = video.get("artist")
                title = video.get("title") or song.name

                if artist and artist != "Unknown Artist" and artist.lower() not in title.lower():
                    filename = f"{title} - {artist}"
                else:
                    filename = title

                filename = sanitize_filename(filename)

                download_song(
                    video["url"],
                    filename
                )

                self.queue.update_filename(
                    song.id,
                    filename + ".mp3"
                )

                self.queue.mark_finished(song.id)

                print(f"Finished: {filename}")

            except Exception as e:
                self.queue.mark_failed(
                    song.id,
                    str(e)
                )
                print(f"Error downloading '{song.name}': {e}")

            time.sleep(0.5)
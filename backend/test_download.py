import sys
from pathlib import Path

# Ensure backend directory is in sys.path
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from search import search_song
from downloader import download_song

song = "Numb Linkin Park"

print(f"Searching for: {song}")
video = search_song(song)
print(f"Found: {video['title']} (URL: {video['url']})")

print("Downloading...")
download_song(video["url"], filename=video["title"])
print("Done!")
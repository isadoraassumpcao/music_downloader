import re
import shutil
from pathlib import Path
from yt_dlp import YoutubeDL
from config import DOWNLOAD_FOLDER, PROJECT_DIR


def sanitize_filename(name: str) -> str:
    """Remove characters not allowed in Windows filenames and clean up spaces."""
    # Remove invalid Windows filename characters: \ / : * ? " < > |
    sanitized = re.sub(r'[\\/:*?"<>|]', "", name)
    # Strip leading/trailing spaces and trailing dots
    sanitized = sanitized.strip(". ")
    return sanitized or "song"


def get_ffmpeg_location() -> str:
    """Find ffmpeg executable from project directory or PATH."""
    local_ffmpeg = PROJECT_DIR / "ffmpeg.exe"
    if local_ffmpeg.is_file():
        return str(local_ffmpeg)
    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        return system_ffmpeg
    return "ffmpeg"


def download_song(video_url: str, filename: str = None) -> bool:
    # Ensure the download folder exists
    DOWNLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

    if filename:
        clean_name = sanitize_filename(filename)
        outtmpl = str(DOWNLOAD_FOLDER / f"{clean_name}.%(ext)s")
    else:
        outtmpl = str(DOWNLOAD_FOLDER / "%(title)s.%(ext)s")

    ffmpeg_loc = get_ffmpeg_location()

    options = {
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "quiet": False,
        "noplaylist": True,
        "ffmpeg_location": ffmpeg_loc,
        "js_runtimes": {"node": {}},
        "remote_components": ["ejs:github"],
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "web_creator", "web_embedded"]
            }
        },
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "320",
        }],
    }

    with YoutubeDL(options) as ydl:
        ydl.download([video_url])

    return True
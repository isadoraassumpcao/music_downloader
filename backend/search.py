from yt_dlp import YoutubeDL


GOOD_WORDS = [
    ("official lyric video", 50),
    ("official lyrics", 45),
    ("official lyric", 40),
    ("lyric video", 30),
    ("lyrics", 20),
    ("lyric", 10),
]

BAD_WORDS = [
    "live",
    "karaoke",
    "nightcore",
    "sped up",
    "slowed",
    "8d",
    "bass boosted",
    "cover",
    "reaction",
    "instrumental",
]


def search_song(song_name: str) -> dict:
    query = f"{song_name} lyrics"

    common_options = {
        "quiet": True,
        "no_warnings": True,
        "js_runtimes": {"node": {}},
        "remote_components": ["ejs:github"],
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "web_creator", "web_embedded"]
            }
        },
    }

    search_options = {
        **common_options,
        "extract_flat": True,
    }

    with YoutubeDL(search_options) as ydl:
        results = ydl.extract_info(
            f"ytsearch20:{query}",
            download=False
        )

    entries = results.get("entries") if results else []
    videos = [v for v in entries if v and v.get("title")]

    if not videos:
        raise ValueError(f"No results found on YouTube for '{song_name}'")

    best_video = None
    best_score = -999

    for video in videos:
        title = video.get("title", "").lower()
        score = 0

        for text, points in GOOD_WORDS:
            if text in title:
                score += points

        for text in BAD_WORDS:
            if text in title:
                score -= 100

        if score > best_score:
            best_score = score
            best_video = video

    if not best_video:
        best_video = videos[0]

    video_url = best_video.get("url") or best_video.get("webpage_url")
    if not video_url and best_video.get("id"):
        video_url = f"https://www.youtube.com/watch?v={best_video['id']}"

    # Try getting full metadata for the chosen video, fallback to search entry if needed
    try:
        with YoutubeDL(common_options) as ydl:
            info = ydl.extract_info(video_url, download=False)
    except Exception:
        info = best_video

    return {
        "url": info.get("webpage_url") or video_url,
        "title": info.get("track") or info.get("title") or best_video.get("title") or song_name,
        "artist": info.get("artist") or info.get("uploader") or best_video.get("uploader") or "Unknown Artist"
    }
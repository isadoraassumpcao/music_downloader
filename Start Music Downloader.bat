@echo off
title Music Downloader

cd /d "C:\Users\Isadora\Desktop\yt-music-downloader"

call .venv\Scripts\activate

start "" cmd /k "cd backend && uvicorn main:app --reload"

timeout /t 3 /nobreak >nul

start "" "frontend\index.html"

exit
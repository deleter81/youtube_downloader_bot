import os
import yt_dlp
import logging
from aiogram import Router

#Папка для загрузок
DOWNLOADS_PATH = "downloads"

if not os.path.exists(DOWNLOADS_PATH):
    os.makedirs(DOWNLOADS_PATH)

logging.basicConfig(level=logging.INFO)

def log_yt_dlp(d):
    if d['status'] == 'finished':
        logging.info(f"✅ Видео загружено: {d['filename']}")
    elif d['status'] == 'error':
        logging.error(f"❌ Ошибка при скачивании: {d.get('error', 'Неизвестная ошибка')}")

def download_video(url):
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOADS_PATH, '%(title)s.%(ext)s'),
        'format': 'best[height<=720]',
        'progress_hooks': [log_yt_dlp],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info_dict)

def register_download_handler(dp):
    router = Router()
    dp.include_router(router)
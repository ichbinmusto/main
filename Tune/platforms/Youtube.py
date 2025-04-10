import asyncio
import os
import re
from typing import Union

import yt_dlp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch

from Tune.utils.database import is_on_off
from Tune.utils.formatters import time_to_seconds


async def shell_cmd(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, errorz = await proc.communicate()
    if errorz:
        errorz_decoded = errorz.decode("utf-8")
        if "unavailable videos are hidden" in errorz_decoded.lower():
            return out.decode("utf-8")
        return errorz_decoded
    return out.decode("utf-8")


cookies_file = "Tune/cookies/cookies.txt"


class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        for message in messages:
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        return text[entity.offset: entity.offset + entity.length]
            if message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        return None

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            vidid = result["id"]
            duration_sec = int(time_to_seconds(duration_min)) if duration_min else 0
            return title, duration_min, duration_sec, thumbnail, vidid
        return None

    async def title(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            return result["title"]

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            return result["duration"]

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            return result["thumbnails"][0]["url"].split("?")[0]

    async def video(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "--cookies", cookies_file,
            "-g",
            "-f", "best[height<=?720][width<=?1280]",
            link,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if stdout:
            return 1, stdout.decode().split("\n")[0]
        return 0, stderr.decode()

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        if videoid:
            link = self.listbase + link
        link = link.split("&")[0]
        playlist = await shell_cmd(
            f"yt-dlp --cookies {cookies_file} -i --get-id --flat-playlist --playlist-end {limit} --skip-download {link}"
        )
        return [key for key in playlist.split("\n") if key]

    async def track(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            return {
                "title": result["title"],
                "link": result["link"],
                "vidid": result["id"],
                "duration_min": result["duration"],
                "thumb": result["thumbnails"][0]["url"].split("?")[0],
            }, result["id"]

    async def formats(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]
        ytdl_opts = {"quiet": True, "cookiefile": cookies_file}
        with yt_dlp.YoutubeDL(ytdl_opts) as ydl:
            formats_available = []
            r = ydl.extract_info(link, download=False)
            for fmt in r.get("formats", []):
                if "dash" not in str(fmt.get("format", "")).lower():
                    if all(k in fmt for k in ["format", "filesize", "format_id", "ext", "format_note"]):
                        formats_available.append({
                            "format": fmt["format"],
                            "filesize": fmt["filesize"],
                            "format_id": fmt["format_id"],
                            "ext": fmt["ext"],
                            "format_note": fmt["format_note"],
                            "yturl": link,
                        })
        return formats_available, link

    async def slider(self, link: str, query_type: int, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]
        results = await VideosSearch(link, limit=10).next()
        result = results.get("result")[query_type]
        return (
            result["title"],
            result["duration"],
            result["thumbnails"][0]["url"].split("?")[0],
            result["id"]
        )

    async def download(
        self,
        link: str,
        mystic,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ) -> Union[str, tuple]:
        if videoid:
            link = self.base + link
        loop = asyncio.get_running_loop()

        def audio_dl():
            opts = {
                "format": "bestaudio/best",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                "cookiefile": cookies_file,
            }
            with yt_dlp.YoutubeDL(opts) as x:
                info = x.extract_info(link, False)
                path = os.path.join("downloads", f"{info['id']}.{info['ext']}")
                if not os.path.exists(path):
                    x.download([link])
            return path

        def video_dl():
            opts = {
                "format": "best[height<=?720][width<=?1280]",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                "cookiefile": cookies_file,
            }
            with yt_dlp.YoutubeDL(opts) as x:
                info = x.extract_info(link, False)
                path = os.path.join("downloads", f"{info['id']}.{info['ext']}")
                if not os.path.exists(path):
                    x.download([link])
            return path

        def song_video_dl():
            opts = {
                "format": f"{format_id}+140",
                "outtmpl": f"downloads/{title}",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                "prefer_ffmpeg": True,
                "merge_output_format": "mp4",
                "cookiefile": cookies_file,
            }
            with yt_dlp.YoutubeDL(opts) as x:
                x.download([link])

        def song_audio_dl():
            opts = {
                "format": format_id,
                "outtmpl": f"downloads/{title}.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                "prefer_ffmpeg": True,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }],
                "cookiefile": cookies_file,
            }
            with yt_dlp.YoutubeDL(opts) as x:
                x.download([link])

        if songvideo:
            await loop.run_in_executor(None, song_video_dl)
            return f"downloads/{title}.mp4"
        elif songaudio:
            await loop.run_in_executor(None, song_audio_dl)
            return f"downloads/{title}.mp3"
        elif video:
            if await is_on_off(1):
                downloaded_file = await loop.run_in_executor(None, video_dl)
                return downloaded_file, True
            proc = await asyncio.create_subprocess_exec(
                "yt-dlp",
                "--cookies", cookies_file,
                "-g",
                "-f", "best[height<=?720][width<=?1280]",
                link,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()
            if stdout:
                return stdout.decode().split("\n")[0], None
            return None
        else:
            downloaded_file = await loop.run_in_executor(None, audio_dl)
            return downloaded_file, True

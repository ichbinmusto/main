import os
import re
import asyncio
from pykeyboard import InlineKeyboard
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from pyrogram.types import (
    Message, InlineKeyboardButton, InlineKeyboardMarkup,
    InputMediaAudio, InputMediaVideo
)
import yt_dlp

from Tune import app, YouTube
from config import BANNED_USERS, SONG_DOWNLOAD_DURATION, SONG_DOWNLOAD_DURATION_LIMIT
from Tune.utils.decorators.language import language, languageCB
from Tune.utils.formatters import convert_bytes
from Tune.utils.inline.song import song_markup

cookies_file = "Tune/cookies/cookies.txt"
SONG_COMMAND = ["song"]


@app.on_message(filters.command(SONG_COMMAND) & filters.group & ~BANNED_USERS)
@language
async def song_command_group(client, message: Message, _):
    upl = InlineKeyboardMarkup([
        [InlineKeyboardButton(text=_["SG_B_1"], url=f"https://t.me/{app.username}?start=song")]
    ])
    await message.reply_text(_["song_1"], reply_markup=upl)



@app.on_message(filters.command(SONG_COMMAND) & filters.private & ~BANNED_USERS)
@language
async def song_command_private(client, message: Message, _):
    await message.delete()
    url = await YouTube.url(message)


    if url:
        if not await YouTube.exists(url):
            return await message.reply_text(_["song_5"])

        mystic = await message.reply_text(_["play_1"])
        try:
            title, duration_min, duration_sec, thumbnail, vidid = await YouTube.details(url)
        except:
            return await mystic.edit_text(_["play_3"])

        if str(duration_min) == "None":
            return await mystic.edit_text(_["song_3"])

        if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
            return await mystic.edit_text(_["play_4"].format(SONG_DOWNLOAD_DURATION, duration_min))

        buttons = song_markup(_, vidid)
        await mystic.delete()
        return await message.reply_photo(thumbnail, caption=_["song_4"].format(title), reply_markup=InlineKeyboardMarkup(buttons))


    elif len(message.command) >= 2:
        mystic = await message.reply_text(_["play_1"])
        query = message.text.split(None, 1)[1]

        try:
            title, duration_min, duration_sec, thumbnail, vidid = await YouTube.details(query)
        except:
            return await mystic.edit_text(_["play_3"])

        if str(duration_min) == "None":
            return await mystic.edit_text(_["song_3"])

        if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
            return await mystic.edit_text(_["play_6"].format(SONG_DOWNLOAD_DURATION, duration_min))

        buttons = song_markup(_, vidid)
        await mystic.delete()
        return await message.reply_photo(thumbnail, caption=_["song_4"].format(title), reply_markup=InlineKeyboardMarkup(buttons))

    else:
        return await message.reply_text(_["song_2"])



@app.on_callback_query(filters.regex("song_back") & ~BANNED_USERS)
@languageCB
async def songs_back_helper(client, CallbackQuery, _):
    _, data = CallbackQuery.data.strip().split(None, 1)
    stype, vidid = data.split("|")
    buttons = song_markup(_, vidid)
    await CallbackQuery.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))



@app.on_callback_query(filters.regex("song_helper") & ~BANNED_USERS)
@languageCB
async def song_helper_cb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer(_["song_6"], show_alert=True)
    except:
        pass

    _, data = CallbackQuery.data.strip().split(None, 1)
    stype, vidid = data.split("|")

    try:
        formats, link = await YouTube.formats(vidid, True)
    except:
        return await CallbackQuery.edit_message_text(_["song_7"])

    keyboard = InlineKeyboard()
    done = []

    if stype == "audio":
        for fmt in formats:
            if "audio" in fmt["format"]:
                if not fmt["filesize"]:
                    continue
                label = fmt["format_note"].title()
                if label in done:
                    continue
                done.append(label)
                size = convert_bytes(fmt["filesize"])
                keyboard.row(
                    InlineKeyboardButton(
                        text=f"{label} Quality Audio = {size}",
                        callback_data=f"song_download {stype}|{fmt['format_id']}|{vidid}"
                    )
                )

    else:
        allowed = [160, 133, 134, 135, 136, 137, 298, 299, 264, 304, 266]
        for fmt in formats:
            if not fmt["filesize"] or int(fmt["format_id"]) not in allowed:
                continue
            size = convert_bytes(fmt["filesize"])
            label = fmt["format"].split("-")[1]
            keyboard.row(
                InlineKeyboardButton(
                    text=f"{label} = {size}",
                    callback_data=f"song_download {stype}|{fmt['format_id']}|{vidid}"
                )
            )

    keyboard.row(
        InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data=f"song_back {stype}|{vidid}"),
        InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")
    )
    await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)



@app.on_callback_query(filters.regex("song_download") & ~BANNED_USERS)
@languageCB
async def song_download_cb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer("Downloading")
    except:
        pass

    _, data = CallbackQuery.data.strip().split(None, 1)
    stype, format_id, vidid = data.split("|")
    mystic = await CallbackQuery.edit_message_text(_["song_8"])
    yturl = f"https://www.youtube.com/watch?v={vidid}"

    with yt_dlp.YoutubeDL({"quiet": True, "cookiefile": cookies_file}) as ytdl:
        info = ytdl.extract_info(yturl, download=False)

    title = re.sub(r"\W+", " ", info["title"]).title()
    duration = info["duration"]
    thumb = await CallbackQuery.message.download()

    if stype == "video":
        try:
            width = CallbackQuery.message.photo.width
            height = CallbackQuery.message.photo.height
        except:
            width = height = 720

        try:
            file_path = await YouTube.download(
                yturl, mystic, songvideo=True, format_id=format_id, title=title
            )
        except Exception as e:
            return await mystic.edit_text(_["song_9"].format(e))

        media = InputMediaVideo(
            media=file_path,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb,
            caption=title,
            supports_streaming=True
        )

        await mystic.edit_text(_["song_11"])
        await app.send_chat_action(CallbackQuery.message.chat.id, ChatAction.UPLOAD_VIDEO)

        try:
            await CallbackQuery.edit_message_media(media=media)
        except Exception as e:
            return await mystic.edit_text(_["song_10"])
        os.remove(file_path)

    elif stype == "audio":
        try:
            filename = await YouTube.download(
                yturl, mystic, songaudio=True, format_id=format_id, title=title
            )
        except Exception as e:
            return await mystic.edit_text(_["song_9"].format(e))

        media = InputMediaAudio(
            media=filename,
            caption=title,
            thumb=thumb,
            title=title,
            performer=info["uploader"]
        )

        await mystic.edit_text(_["song_11"])
        await app.send_chat_action(CallbackQuery.message.chat.id, ChatAction.UPLOAD_AUDIO)

        try:
            await CallbackQuery.edit_message_media(media=media)
        except Exception as e:
            return await mystic.edit_text(_["song_10"])
        os.remove(filename)

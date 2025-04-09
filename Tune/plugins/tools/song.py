import os
import re
import yt_dlp

from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.enums import ChatAction
from pyrogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, InputMediaAudio,
    InputMediaVideo, Message
)

from Tune import app, YouTube
from config import BANNED_USERS, SONG_DOWNLOAD_DURATION, SONG_DOWNLOAD_DURATION_LIMIT
from Tune.utils.decorators.language import language, languageCB
from Tune.utils.formatters import convert_bytes
from Tune.utils.inline.song import song_markup

cookies_file = "Tune/cookies/cookies.txt"

@app.on_message(filters.command("song") & filters.group & ~BANNED_USERS)
@language
async def song_commad_group(client, message: Message, _):
    buttons = [[InlineKeyboardButton(text=_["SG_B_1"], url=f"https://t.me/{app.username}?start=song")]]
    await message.reply_text(_["song_1"], reply_markup=InlineKeyboardMarkup(buttons))


@app.on_message(filters.command(["song"]) & filters.private & ~BANNED_USERS)
@language
async def song_commad_private(client, message: Message, _):
    await message.delete()
    url = await YouTube.url(message)

    if url and not await YouTube.exists(url):
        return await message.reply_text(_["song_5"])

    mystic = await message.reply_text(_["play_1"])

    if url:
        details_query = url
    elif len(message.command) >= 2:
        details_query = message.text.split(None, 1)[1]
    else:
        return await message.reply_text(_["song_2"])

    try:
        title, duration_min, duration_sec, thumbnail, vidid = await YouTube.details(details_query)
    except:
        return await mystic.edit_text(_["play_3"])

    if str(duration_min) == "None":
        return await mystic.edit_text(_["song_3"])
    if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
        return await mystic.edit_text(_["play_4" if url else "play_6"].format(SONG_DOWNLOAD_DURATION, duration_min))

    await mystic.delete()
    return await message.reply_photo(
        thumbnail,
        caption=_["song_4"].format(title),
        reply_markup=InlineKeyboardMarkup(song_markup(_, vidid)),
    )


@app.on_callback_query(filters.regex("song_back") & ~BANNED_USERS)
@languageCB
async def songs_back_helper(client, CallbackQuery, _):
    _, data = CallbackQuery.data.strip().split(None, 1)
    stype, vidid = data.split("|")
    await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(song_markup(_, vidid))
    )


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
        formats, _ = await YouTube.formats(vidid, True)
    except:
        return await CallbackQuery.edit_message_text(_["song_7"])

    keyboard = InlineKeyboard()
    done = []

    for x in formats:
        if x["filesize"] is None:
            continue

        if stype == "audio":
            if "audio" not in x["format"]:
                continue
            form = x["format_note"].title()
            if form in done:
                continue
            done.append(form)
            text = f"{form} Quality Audio = {convert_bytes(x['filesize'])}"
        else:
            if int(x["format_id"]) not in [160, 133, 134, 135, 136, 137, 298, 299, 264, 304, 266]:
                continue
            text = f"{x['format'].split('-')[1]} = {convert_bytes(x['filesize'])}"

        keyboard.row(
            InlineKeyboardButton(
                text=text,
                callback_data=f"song_download {stype}|{x['format_id']}|{vidid}"
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

    title = re.sub(r"\W+", " ", info["title"].title())
    duration = info["duration"]
    thumb = await CallbackQuery.message.download()

    if stype == "video":
        width, height = CallbackQuery.message.photo.width, CallbackQuery.message.photo.height
        try:
            file_path = await YouTube.download(yturl, mystic, songvideo=True, format_id=format_id, title=title)
        except Exception as e:
            return await mystic.edit_text(_["song_9"].format(e))

        await mystic.edit_text(_["song_11"])
        await app.send_chat_action(chat_id=CallbackQuery.message.chat.id, action=ChatAction.UPLOAD_VIDEO)
        try:
            await CallbackQuery.edit_message_media(media=InputMediaVideo(
                media=file_path, duration=duration, width=width, height=height,
                thumb=thumb, caption=title, supports_streaming=True
            ))
        except Exception as e:
            print(e)
            return await mystic.edit_text(_["song_10"])
        os.remove(file_path)

    else:
        try:
            filename = await YouTube.download(yturl, mystic, songaudio=True, format_id=format_id, title=title)
        except Exception as e:
            return await mystic.edit_text(_["song_9"].format(e))

        await mystic.edit_text(_["song_11"])
        await app.send_chat_action(chat_id=CallbackQuery.message.chat.id, action=ChatAction.UPLOAD_AUDIO)
        try:
            await CallbackQuery.edit_message_media(media=InputMediaAudio(
                media=filename, caption=title, thumb=thumb,
                title=title, performer=info["uploader"]
            ))
        except Exception as e:
            print(e)
            return await mystic.edit_text(_["song_10"])
        os.remove(filename)

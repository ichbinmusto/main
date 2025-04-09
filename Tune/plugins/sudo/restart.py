import asyncio
import os
import sys
import shutil
import socket
import logging
from datetime import datetime

import urllib3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from pyrogram import filters

import config
from Tune import app
from Tune.misc import HAPP, SUDOERS, XCB
from Tune.utils.database import (
    get_active_chats,
    remove_active_chat,
    remove_active_video_chat,
)
from Tune.utils.decorators.language import language
from Tune.utils.pastebin import JarvisBin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def restart_bot():
    """Gracefully restart the bot."""
    os.execv(sys.executable, ['python'] + sys.argv)

async def is_heroku():
    return "heroku" in socket.getfqdn()

@app.on_message(filters.command(["getlog", "logs", "getlogs"]) & SUDOERS)
@language
async def log_(client, message, _):
    try:
        await message.reply_document(document="log.txt")
    except Exception as e:
        logger.exception("Failed to send logs:")
        await message.reply_text(_["server_1"])

@app.on_message(filters.command(["update", "gitpull"]) & SUDOERS)
@language
async def update_(client, message, _):
    response = await message.reply_text(_["server_3"])

    try:
        repo = Repo()
    except GitCommandError:
        return await response.edit(_["server_4"])
    except InvalidGitRepositoryError:
        return await response.edit(_["server_5"])

    os.system(f"git fetch origin {config.UPSTREAM_BRANCH} &> /dev/null")
    await asyncio.sleep(7)

    REPO_ = repo.remotes.origin.url.split(".git")[0]
    updates = ""
    commits = list(repo.iter_commits(f"HEAD..origin/{config.UPSTREAM_BRANCH}"))

    if not commits:
        return await response.edit(_["server_6"])

    ordinal = lambda d: "%d%s" % (
        d,
        "tsnrhtdd"[(d // 10 % 10 != 1) * (d % 10 < 4) * d % 10 :: 4],
    )

    for info in commits:
        updates += (
            f"<b>➣ #{info.count()}: <a href={REPO_}/commit/{info}>{info.summary}</a> ʙʏ -> {info.author}</b>\n"
            f"\t\t\t\t<b>➥ ᴄᴏᴍᴍɪᴛᴇᴅ ᴏɴ :</b> {ordinal(int(datetime.fromtimestamp(info.committed_date).strftime('%d')))} "
            f"{datetime.fromtimestamp(info.committed_date).strftime('%b')}, "
            f"{datetime.fromtimestamp(info.committed_date).strftime('%Y')}\n\n"
        )

    update_text = "<b>ᴀ ɴᴇᴡ ᴜᴩᴅᴀᴛᴇ ɪs ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ᴛʜᴇ ʙᴏᴛ !</b>\n\n➣ ᴩᴜsʜɪɴɢ ᴜᴩᴅᴀᴛᴇs ɴᴏᴡ\n\n<b><u>ᴜᴩᴅᴀᴛᴇs:</u></b>\n\n"
    final_text = update_text + updates

    if len(final_text) > 4096:
        url = await JarvisBin(updates)
        nrs = await response.edit(
            f"{update_text}<a href={url}>ᴄʜᴇᴄᴋ ᴜᴩᴅᴀᴛᴇs</a>",
            disable_web_page_preview=True
        )
    else:
        nrs = await response.edit(final_text, disable_web_page_preview=True)

    os.system("git stash &> /dev/null && git pull")

    try:
        served_chats = await get_active_chats()
        for x in served_chats:
            try:
                await app.send_message(
                    chat_id=int(x),
                    text=_["server_8"].format(app.mention),
                )
                await remove_active_chat(x)
                await remove_active_video_chat(x)
            except Exception as e:
                logger.warning(f"Failed to notify or remove chat {x}: {e}")
        await response.edit(f"{nrs.text}\n\n{_['server_7']}")
    except Exception as e:
        logger.exception("Failed during post-update cleanup:")

    # VPS RESTART LOGIC
    os.system("pip3 install -r requirements.txt")
    restart_bot()

@app.on_message(filters.command(["restart"]) & SUDOERS)
async def restart_(_, message):
    response = await message.reply_text("ʀᴇsᴛᴀʀᴛɪɴɢ...")

    ac_chats = await get_active_chats()
    for x in ac_chats:
        try:
            await app.send_message(
                chat_id=int(x),
                text=f"{app.mention} ɪs ʀᴇsᴛᴀʀᴛɪɴɢ...\n\nʏᴏᴜ ᴄᴀɴ sᴛᴀʀᴛ ᴩʟᴀʏɪɴɢ ᴀɢᴀɪɴ ᴀғᴛᴇʀ 15-20 sᴇᴄᴏɴᴅs.",
            )
            await remove_active_chat(x)
            await remove_active_video_chat(x)
        except Exception as e:
            logger.warning(f"Failed to notify or remove chat {x}: {e}")

    # Clean directories
    for folder in ["downloads", "raw_files", "cache"]:
        shutil.rmtree(folder, ignore_errors=True)

    await response.edit_text(
        "» ʀᴇsᴛᴀʀᴛ ᴘʀᴏᴄᴇss sᴛᴀʀᴛᴇᴅ, ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ғᴏʀ ғᴇᴡ sᴇᴄᴏɴᴅs..."
    )

    restart_bot()

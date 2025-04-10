𝐅𝐨𝐫𝐞𝐯𝐞𝐫 𝐂𝐫𝐮𝐬𝐡 🤎:
import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

# Load environment variables from .env file
load_dotenv()

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")

# Specify where to get the following credentials
OWNER_USERNAME = getenv("OWNER_USERNAME", "Vansam53")
BOT_USERNAME = getenv("BOT_USERNAME", "Vanshikamusic_bot")
BOT_NAME = getenv("BOT_NAME", "⌜Vanshika music⌟ 🜲 💗 [ɴᴏ ᴀᴅs]")
ASSUSERNAME = getenv("ASSUSERNAME", None)
EVALOP = list(map(int, getenv("EVALOP", "7549352044").split()))
MONGO_DB_URI = getenv("MONGO_DB_URI", None)
LOGGER_ID = int(getenv("LOGGER_ID", -1002542498289))
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 600))

GPT_API = getenv("GPT_API")
DEEP_API = getenv("DEEP_API")
OWNER_ID = int(getenv("OWNER_ID", 7492415764))

# Heroku deployment settings - Refer to Heroku documentation on how to obtain these
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/Naincysoni21/Radhamusicz")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "Master")
GIT_TOKEN = getenv("GIT_TOKEN", None)

# Support and contact information - Provide your own support channels
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/NAINCY_UPDATES")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/RADHA_MUSIC_SUPPORT")

# Set this to True if you want the assistant to automatically leave chats after an interval
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))
AUTO_LEAVE_ASSISTANT_TIME = int(getenv("ASSISTANT_LEAVE_TIME", "11500"))

# Server limits and configurations - These can be set based on your server configurations
SERVER_PLAYLIST_LIMIT = int(getenv("SERVER_PLAYLIST_LIMIT", "3000"))
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "2500"))
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION", "9999999"))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "9999999"))

# External service credentials - Obtain these from Spotify
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "22b6125bfe224587b722d6815002db2b")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "c9c63c6fbf2f467c8bc68624851e9773")

# Telegram file size limits - Set these according to your requirements
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "5242880000"))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "5242880000"))

# Pyrogram session strings - You need to generate these yourself
STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)

# Bot introduction messages - These can be customized as per your preference
AYU = [
    "💞", "🦋", "🔍", "🧪", "🦋", "⚡️", "🔥", "🦋", "🎩", "🌈", "🍷", "🥂", "🦋", "🥃", "🥤", "🕊️",
    "🦋", "🦋", "🕊️", "🦋", "🕊️", "🦋", "🦋", "🦋", "🪄", "💌", "🦋", "🦋", "🧨"
]

AYUV = [
    "ʜᴇʟʟᴏ {0}, 🥀\n\n ɪᴛ'ꜱ ᴍᴇ {1} !\n\n┏━━━━━━━━━━━━━━━━━⧫\n┠ ◆ ꜱᴜᴘᴘᴏʀᴛɪɴɢ ᴘʟᴀᴛꜰᴏʀᴍꜱ : ʏᴏᴜᴛᴜʙᴇ, ꜱᴘᴏᴛɪꜰʏ,\n┠ ◆ ʀᴇꜱꜱᴏ, ᴀᴘᴘʟᴇᴍᴜꜱɪᴄ , ꜱᴏᴜɴᴅᴄʟᴏᴜᴅ ᴇᴛᴄ.\n┗━━━━━━━━━━━━━━━━━⧫\n┏━━━━━━━━━━━━━━━━━⧫\n┠ ➥ Uᴘᴛɪᴍᴇ : {2}\n┠ ➥ SᴇʀᴠᴇʀSᴛᴏʀᴀɢᴇ : {3}\n┠ ➥ CPU Lᴏᴀᴅ : {4}\n┠ ➥ RAM Cᴏɴsᴜᴘᴛɪᴏɴ : {5}\n┠ ➥ ᴜꜱᴇʀꜱ : {6}\n┠ ➥ ᴄʜᴀᴛꜱ : {7}\n┗━━━━━━━━━━━━━━━━━⧫\n\n🫧 ᴅᴇᴠᴇʟᴏᴩᴇʀ 🪽 ➪ [Dᴇᴠᴇʟᴏᴘᴇʀ💗](https://t.me/Vansam53)",
    "ʜɪɪ, {0} ~\n\n◆ ɪ'ᴍ ᴀ {1} ᴛᴇʟᴇɢʀᴀᴍ ꜱᴛʀᴇᴀᴍɪɴɢ ʙᴏᴛ ᴡɪᴛʜ ꜱᴏᴍᴇ ᴜꜱᴇꜰᴜʟ\n◆ ᴜʟᴛʀᴀ ғᴀsᴛ ᴠᴄ ᴘʟᴀʏᴇʀ ꜰᴇᴀᴛᴜʀᴇꜱ.\n\n✨ ꜰᴇᴀᴛᴜʀᴇꜱ ⚡️\n◆ ʙᴏᴛ ғᴏʀ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴘs.\n◆ Sᴜᴘᴇʀғᴀsᴛ ʟᴀɢ Fʀᴇᴇ ᴘʟᴀʏᴇʀ.\n◆ ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ ᴍᴜꜱɪᴄ + ᴠɪᴅᴇᴏ.\n◆ ʟɪᴠᴇ ꜱᴛʀᴇᴀᴍɪɴɢ.\n◆ ɴᴏ ᴘʀᴏᴍᴏ.\n◆ ʙᴇꜱᴛ ꜱᴏᴜɴᴅ Qᴜᴀʟɪᴛʏ.\n◆ 24×7 ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ ᴍᴜꜱɪᴄ.\n◆ ᴀᴅᴅ ᴛʜɪꜱ ʙᴏᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴍᴀᴋᴇ ɪᴛ ᴀᴅᴍɪɴ ᴀɴᴅ ᴇɴᴊᴏʏ ᴍᴜꜱɪᴄ 🎵.\n\n┏━━━━━━━━━━━━━━━━━⧫\n┠ ◆ ꜱᴜᴘᴘᴏʀᴛɪɴɢ ᴘʟᴀᴛꜰᴏʀᴍꜱ : ʏᴏᴜᴛᴜʙᴇ, ꜱᴘᴏᴛɪꜰʏ,\n┠ ◆ ʀᴇꜱꜱᴏ, ᴀᴘᴘʟᴇᴍᴜꜱɪᴄ , ꜱᴏᴜɴᴅᴄʟᴏᴜᴅ ᴇᴛᴄ.\n┗━━━━━━━━━━━━━━━━━⧫\n┏━━━━━━━━━━━━━━━━━⧫\n┠ ➥ Uᴘᴛɪᴍᴇ : {2}\n┠ ➥ SᴇʀᴠᴇʀSᴛᴏʀᴀɢᴇ : {3}\n┠ ➥ CPU Lᴏᴀᴅ : {4}\n┠ ➥ RAM Cᴏɴsᴜᴘᴛɪᴏɴ : {5}\n┠ ➥ ᴜꜱᴇʀꜱ : {6}\n┠ ➥ ᴄʜᴀᴛꜱ : {7}\n┗━━━━━━━━━━━━━━━━━⧫\n\n🫧 ᴅᴇᴠᴇʟᴏᴩᴇʀ 🪽 ➪ [Dᴇᴠᴇʟᴏᴘᴇʀ💗](https://t.me/Vansam53)",
    "ʜᴇʟʟᴏ {0}, 🥀\n\n ɪᴛ'ꜱ ᴍᴇ {1} !\n\n┏━━━━━━━━━━━━━━━━━⧫\n┠ ◆ ꜱᴜᴘᴘᴏʀᴛɪɴɢ ᴘʟᴀᴛꜰᴏʀᴍꜱ : ʏᴏᴜᴛᴜʙᴇ, ꜱᴘᴏᴛɪꜰʏ,\n┠ ◆ ʀᴇꜱꜱᴏ, ᴀᴘᴘʟᴇᴍᴜꜱɪᴄ , ꜱᴏᴜɴᴅᴄʟᴏᴜᴅ ᴇᴛᴄ.\n┗━━━━━━━━━━━━━━━━━⧫\n┏━━━━━━━━━━━━━━━━━⧫\n┠ ➥ Uᴘᴛɪᴍᴇ : {2}\n┠ ➥ SᴇʀᴠᴇʀSᴛᴏʀᴀɢᴇ : {3}\n┠ ➥ CPU Lᴏᴀᴅ : {4}\n┠ ➥ RAM Cᴏɴsᴜᴘᴛɪᴏɴ : {5}\n┠ ➥ ᴜꜱᴇʀꜱ : {6}\n┠ ➥ ᴄʜᴀᴛꜱ : {7}\n┗━━━━━━━━━━━━━━━━━⧫\n\n🫧 ᴅᴇᴠᴇʟᴏᴩᴇʀ 🪽 ➪ [Dᴇᴠᴇʟᴏᴘᴇʀ💗](https://t.me/Vansam53)",
    "ʜɪɪ, {0} ~\n\n◆ ɪ'ᴍ ᴀ {1} ᴛᴇʟᴇɢʀᴀᴍ ꜱᴛʀᴇᴀᴍɪɴɢ ʙᴏᴛ ᴡɪᴛʜ ꜱᴏᴍᴇ ᴜꜱᴇꜰᴜʟ\n◆ ᴜʟᴛʀᴀ ғᴀsᴛ ᴠᴄ ᴘʟᴀʏᴇʀ ꜰᴇᴀᴛᴜʀᴇꜱ.\n\n✨ ꜰᴇᴀᴛᴜʀᴇꜱ ⚡️\n◆ ʙᴏᴛ ғᴏʀ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴘs.\n◆ Sᴜᴘᴇʀғᴀsᴛ ʟᴀɢ Fʀᴇᴇ ᴘʟᴀʏᴇʀ.\n◆ ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ ᴍᴜꜱɪᴄ + ᴠɪᴅᴇᴏ.\n◆ ʟɪᴠᴇ ꜱᴛʀᴇᴀᴍɪɴɢ.\n◆ ɴᴏ ᴘʀᴏᴍᴏ.\n◆ ʙᴇꜱᴛ ꜱᴏᴜɴᴅ Qᴜᴀʟɪᴛʏ.\n◆ 24×7 ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ ᴍᴜꜱɪᴄ.\n◆ ᴀᴅᴅ ᴛʜɪꜱ ʙᴏᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴍᴀᴋᴇ ɪᴛ ᴀᴅᴍɪɴ ᴀɴᴅ ᴇɴᴊᴏʏ ᴍᴜꜱɪᴄ 🎵.\n\n┏━━━━━━━━━━━━━━━━━⧫\n┠ ◆ ꜱᴜᴘᴘᴏʀᴛɪɴɢ ᴘʟᴀᴛꜰᴏʀᴍꜱ : ʏᴏᴜᴛᴜʙᴇ, ꜱᴘᴏᴛɪꜰʏ,\n┠ ◆ ʀᴇꜱꜱᴏ, ᴀᴘᴘʟᴇᴍᴜꜱɪᴄ , ꜱᴏᴜɴᴅᴄʟᴏᴜᴅ ᴇᴛᴄ.\n┗━━━━━━━━━━━━━━━━━⧫\n┏━━━━━━━━━━━━━━━━━⧫\n┠ ➥ Uᴘᴛɪᴍᴇ : {2}\n┠ ➥ SᴇʀᴠᴇʀSᴛᴏʀᴀɢᴇ : {3}\n┠ ➥ CPU Lᴏᴀᴅ : {4}\n┠ ➥ RAM Cᴏɴsᴜᴘᴛɪᴏɴ : {5}\n┠ ➥ ᴜꜱᴇʀꜱ : {6}\n┠ ➥ ᴄʜᴀᴛꜱ : {7}\n┗━━━━━━━━━━━━━━━━━⧫\n\n🫧 ᴅᴇᴠᴇʟᴏᴩᴇʀ 🪽 ➪ [Dᴇᴠᴇʟᴏᴘᴇʀ💗](https://t.me/Vansam53)",
    "ʜᴇʟʟᴏ {0}, 🥀\n\n ɪᴛ'ꜱ ᴍᴇ {1} !\n\n┏━━━━━━━━━━━━━━━━━⧫\n┠ ◆ ꜱᴜᴘᴘᴏʀᴛɪɴɢ ᴘʟᴀᴛꜰᴏʀᴍꜱ : ʏᴏᴜᴛᴜʙᴇ, ꜱᴘᴏᴛɪꜰʏ,\n┠ ◆ ʀᴇꜱꜱᴏ, ᴀᴘᴘʟᴇᴍᴜꜱɪᴄ , ꜱᴏᴜɴᴅᴄʟᴏᴜᴅ ᴇᴛᴄ.\n┗━━━━━━━━━━━━━━━━━⧫\n┏━━━━━━━━━━━━━━━━━⧫\n┠ ➥ Uᴘᴛɪᴍᴇ : {2}\n┠ ➥ SᴇʀᴠᴇʀSᴛᴏʀᴀɢᴇ : {3}\n┠ ➥ CPU Lᴏᴀᴅ : {4}\n┠ ➥ RAM Cᴏɴsᴜᴘᴛɪᴏɴ : {5}\n┠ ➥ ᴜꜱᴇʀꜱ : {6}\n┠ ➥ ᴄʜᴀᴛꜱ : {7}\n┗━━━━━━━━━━━━━━━━━⧫\n\n🫧 ᴅᴇᴠᴇʟᴏᴩᴇʀ 🪽 ➪ [Dᴇᴠᴇʟᴏᴘᴇʀ💗](https://t.me/Vansam53)"
]

BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

START_IMG_URL = getenv(
    "START_IMG_URL", "https://envs.sh/L0j.jpg"
)
PING_VID_URL = getenv(
    "PING_VID_URL", "https://envs.sh/ysj.mp4"
)
PLAYLIST_IMG_URL = "https://envs.sh/L0_.jpg"
STATS_VID_URL = "https://envs.sh/ysK.mp4"
TELEGRAM_AUDIO_URL = "https://envs.sh/L0A.jpg"
TELEGRAM_VIDEO_URL = "https://envs.sh/L0A.jpg"
STREAM_IMG_URL = "https://envs.sh/L0A.jpg"
SOUNCLOUD_IMG_URL = "https://envs.sh/L0A.jpg"
YOUTUBE_IMG_URL = "https://envs.sh/L0p.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://envs.sh/L0p.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://envs.sh/L0p.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://envs.sh/L0p.jpg"

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
)

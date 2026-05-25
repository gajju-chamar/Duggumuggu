import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_STRING = os.getenv("SESSION_STRING")
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "Owner")

SUDO_USERS = [int(x.strip()) for x in os.getenv("SUDO_USERS", "").split(",") if x.strip()]
ALLOWED_CHATS = [int(x.strip()) for x in os.getenv("ALLOWED_CHATS", "").split(",") if x.strip()]
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

FFMPEG_OPTIONS = (
    "-vn -b:a 128k -c:a libopus -vbr on "
    "-compression_level 10 -application lowdelay "
    "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
)
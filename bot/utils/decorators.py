from pyrogram import Client
from pyrogram.types import Message
from bot.core.config import SUDO_USERS, ALLOWED_CHATS, OWNER_USERNAME
from functools import wraps

def sudo_and_chat_restricted(func):
    @wraps(func)
    async def wrapper(client: Client, message: Message):
        if message.chat.type.name in ["GROUP", "SUPERGROUP"]:
            if message.chat.id not in ALLOWED_CHATS:
                return
        
        if message.from_user.id not in SUDO_USERS:
            await message.reply_text(f"You don't have access, ask @{OWNER_USERNAME} for approving you.")
            return
            
        return await func(client, message)
    return wrapper
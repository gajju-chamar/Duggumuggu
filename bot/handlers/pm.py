from pyrofork import Client, filters
from pyrofork.types import Message
from bot.utils.decorators import sudo_and_chat_restricted

@Client.on_message(filters.private & filters.command("start"))
@sudo_and_chat_restricted
async def pm_awake(client: Client, message: Message):
    await message.reply_text("✅ The VC Music Bot is awake and running efficiently.")
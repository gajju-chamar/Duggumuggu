from pyrogram import Client, filters
from bot.database.redis_cache import get_queue, clear_queue, remove_specific_track
from bot.utils.ui_formatters import queue_ui
from bot.utils.decorators import sudo_and_chat_restricted

@Client.on_message(filters.command("queue") & filters.group)
@sudo_and_chat_restricted
async def show_queue(client: Client, message):
    queue = await get_queue(message.chat.id)
    if not queue:
        return await message.reply_text("The queue is currently empty.")
    
    text, markup = queue_ui(queue[1:]) 
    await message.reply_text(text, reply_markup=markup)

@Client.on_message(filters.command("clear") & filters.group)
@sudo_and_chat_restricted
async def clear_queue_cmd(client: Client, message):
    if len(message.command) == 1:
        await clear_queue(message.chat.id)
        return await message.reply_text("🧹 Entire queue cleared.")
    
    try:
        index = int(message.command[1])
        success = await remove_specific_track(message.chat.id, index)
        if success:
            await message.reply_text(f"🧹 Removed track {index} from queue.")
        else:
            await message.reply_text("❌ Invalid queue number.")
    except ValueError:
        await message.reply_text("❌ Please provide a valid number. (e.g., /clear 2)")
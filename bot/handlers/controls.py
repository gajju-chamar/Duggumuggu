from pyrofork import Client, filters
from bot.database.redis_cache import get_queue, clear_queue, pop_queue, add_to_queue
from bot.utils.decorators import sudo_and_chat_restricted
from bot.handlers.play import start_stream

@Client.on_message(filters.command("pause") & filters.group)
@sudo_and_chat_restricted
async def pause_cmd(client, message):
    try:
        await client.call_py.pause_stream(message.chat.id)
        await message.reply_text("⏸ Stream paused.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@Client.on_message(filters.command("resume") & filters.group)
@sudo_and_chat_restricted
async def resume_cmd(client, message):
    try:
        await client.call_py.resume_stream(message.chat.id)
        await message.reply_text("▶️ Stream resumed.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@Client.on_message(filters.command("stop") & filters.group)
@sudo_and_chat_restricted
async def stop_cmd(client, message):
    try:
        await clear_queue(message.chat.id)
        await client.call_py.leave_group_call(message.chat.id)
        await message.reply_text("⏹ Stream stopped and queue cleared.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@Client.on_message(filters.command("skip") & filters.group)
@sudo_and_chat_restricted
async def skip_cmd(client, message):
    try:
        await pop_queue(message.chat.id)
        next_track = await pop_queue(message.chat.id)
        if next_track:
            await add_to_queue(message.chat.id, next_track)
            await start_stream(client, message.chat.id, next_track, None)
            await message.reply_text("⏭ Skipped to next track.")
        else:
            await client.call_py.leave_group_call(message.chat.id)
            await message.reply_text("⏭ Skipped. Queue is empty, leaving VC.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
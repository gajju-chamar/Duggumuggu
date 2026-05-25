import asyncio
import uvloop
from pyrogram import Client
from pyrogram.types import BotCommand
from pytgcalls import PyTgCalls
from bot.core.config import API_ID, API_HASH, BOT_TOKEN, SESSION_STRING
import bot.handlers.pm
import bot.handlers.play
import bot.handlers.controls
import bot.handlers.queue_cmd

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

app = Client("vc_music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_app = Client("vc_user_session", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
call_py = PyTgCalls(user_app)

async def main():
    await app.start()
    await user_app.start()
    await call_py.start()
    
    await app.set_bot_commands([
        BotCommand("play", "Play a song or add to queue"),
        BotCommand("pause", "Pause the current stream"),
        BotCommand("resume", "Resume the paused stream"),
        BotCommand("skip", "Skip to the next track"),
        BotCommand("stop", "Stop playback and clear queue"),
        BotCommand("queue", "Show the current music queue"),
        BotCommand("clear", "Clear the queue or a specific track"),
        BotCommand("ping", "Check bot uptime and latency")
    ])
    
    print("🚀 VC Music Bot is alive and highly optimized.")
    app.call_py = call_py 
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
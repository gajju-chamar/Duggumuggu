from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls.types import AudioQuality, Update
from pytgcalls.types.stream import StreamAudioEnded
from pytgcalls.types.input_stream import AudioPiped, AudioParameters
from bot.streaming.yt_dlp_engine import extract_audio_info
from bot.database.redis_cache import add_to_queue, get_queue, pop_queue
from bot.utils.ui_formatters import playing_now_ui
from bot.utils.decorators import sudo_and_chat_restricted
import asyncio

@Client.on_message(filters.command("play") & filters.group)
@sudo_and_chat_restricted
async def play_command(client: Client, message: Message):
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply_text("Please provide a song name or URL.")
    
    m = await message.reply_text("🔍 Searching... optimizing stream parameters...")
    
    try:
        track_data = await extract_audio_info(query)
        track_data['req_by'] = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
        
        queue = await get_queue(message.chat.id)
        await add_to_queue(message.chat.id, track_data)
        
        if len(queue) == 0:
            await start_stream(client, message.chat.id, track_data, m)
        else:
            await m.edit_text(f"✅ Added to Queue: **{track_data['title']}**")
            
    except Exception as e:
        await m.edit_text(f"❌ Error: {str(e)}")

async def start_stream(client: Client, chat_id: int, track_data: dict, message_obj: Message = None):
    stream = AudioPiped(
        track_data['url'],
        AudioParameters(bitrate=128000)
    )
    
    try:
        if client.call_py.get_call(chat_id):
            await client.call_py.change_stream(chat_id, stream)
        else:
            await client.call_py.join_group_call(chat_id, stream, stream_type=AudioQuality.HIGH)
            
        text, markup = playing_now_ui(
            track_data['title'], 
            track_data['artist'], 
            track_data['duration_str'], 
            track_data['req_by']
        )
        
        if message_obj:
            await message_obj.edit_text(text, reply_markup=markup)
        else:
            await client.send_message(chat_id, text, reply_markup=markup)
            
    except Exception as e:
        if message_obj:
            await message_obj.edit_text(f"❌ Stream Error: {str(e)}")
        else:
            await client.send_message(chat_id, f"❌ Stream Error: {str(e)}")

@Client.on_raw_update() 
async def stream_end_handler(client: Client, update: Update, users, chats):
    if isinstance(update, StreamAudioEnded):
        chat_id = update.chat_id
        try:
            await pop_queue(chat_id) 
            next_track = await pop_queue(chat_id) 
            
            if next_track:
                await add_to_queue(chat_id, next_track)
                await start_stream(client, chat_id, next_track, None)
            else:
                await client.call_py.leave_group_call(chat_id)
        except Exception as e:
            await client.send_message(chat_id, "⚠️ Reached end of queue or encountered an error. Leaving VC.")
            await client.call_py.leave_group_call(chat_id)
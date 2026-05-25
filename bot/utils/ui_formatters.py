from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def playing_now_ui(title: str, artist: str, duration: str, requested_by: str, status: str = "Playing...") -> tuple[str, InlineKeyboardMarkup]:
    text = f"""╭──────────────────╮
│ 🎧 PLAYING NOW
╰──────────────────╯

🎵 {title}
👤 {artist}
⏱ {duration}

📥 Requested by: {requested_by}
🔊 Volume: 100%

━━━━━━━━━━━━━━━━━━
▶ {status}
━━━━━━━━━━━━━━━━━━"""

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("⏸ Pause", callback_data="cb_pause"), InlineKeyboardButton("⏭ Skip", callback_data="cb_skip")],
        [InlineKeyboardButton("📜 Queue", callback_data="cb_queue"), InlineKeyboardButton("⏹ Stop", callback_data="cb_stop")]
    ])
    return text, markup

def queue_ui(queue: list) -> tuple[str, InlineKeyboardMarkup]:
    text = """╭──────────────────╮
│ 📜 MUSIC QUEUE
╰──────────────────╯\n\n"""

    for idx, track in enumerate(queue, 1):
        text += f"{idx}. {track['title']}\n⏱ {track['duration_str']}\n\n"

    text += f"""━━━━━━━━━━━━━━━━━━
🎵 Total Tracks: {len(queue)}
━━━━━━━━━━━━━━━━━━"""

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("⏭ Skip", callback_data="cb_skip"), InlineKeyboardButton("🧹 Clear", callback_data="cb_clear")],
        [InlineKeyboardButton("⬅ Back", callback_data="cb_back")]
    ])
    return text, markup
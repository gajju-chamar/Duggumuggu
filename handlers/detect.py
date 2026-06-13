from langdetect import detect
async def detect_lang(update, context):
    if not update.message.reply_to_message:
        return await update.message.reply_text("Reply to a message.")
    text = update.message.reply_to_message.text or update.message.reply_to_message.caption
    await update.message.reply_text(f"Detected: {detect(text)}")

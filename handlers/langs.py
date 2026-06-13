from languages import LANGUAGES
async def langs(update, context):
    await update.message.reply_text("\n".join(f"{k} - {v}" for k,v in LANGUAGES.items()))

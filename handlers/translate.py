from translator import translate_text
from languages import LANGUAGES

async def translate(update, context):
    if not update.message.reply_to_message:
        return await update.message.reply_text("Reply to a message.")
    if not context.args:
        return await update.message.reply_text("Usage: /tr en")

    lang = context.args[0].lower()
    if lang not in LANGUAGES:
        return await update.message.reply_text("Unsupported language")

    text = update.message.reply_to_message.text or update.message.reply_to_message.caption
    result = translate_text(text, lang)
    await update.message.reply_text(result)

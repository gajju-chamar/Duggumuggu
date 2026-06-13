from telegram.ext import Application, CommandHandler
from config import BOT_TOKEN
from handlers.start import start
from handlers.translate import translate
from handlers.detect import detect_lang
from handlers.langs import langs

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("tr", translate))
app.add_handler(CommandHandler("detect", detect_lang))
app.add_handler(CommandHandler("langs", langs))

if __name__ == "__main__":
    app.run_polling()

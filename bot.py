from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import threading
from flask import Flask

TOKEN = "8746114474:AAEis62cyRb-ZsIPal0LgD9D22E9tBVbr9I"

app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Bot is running!"

async def start(update, context):
    await update.message.reply_text("Hello! Bot is ready!")

async def echo(update, context):
    await update.message.reply_text(update.message.text)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, echo))

threading.Thread(target=lambda: app_flask.run(host='0.0.0.0', port=8080)).start()
app.run_polling()

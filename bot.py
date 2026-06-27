import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("TOKEN", "8746114474:AAEis62cyRb-ZsIPal0LgD9D22E9tBVbr9I")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(
            "🎯 باز کن F1VRA Airdrop",
            web_app=WebAppInfo(url="https://jazzy-pixie-6169f8.netlify.app/")
        )]
    ]
    await update.message.reply_text(
        "🎁 *به F1VRA Airdrop خوش اومدی!*\n\nدکمه رو بزن و شروع کن! 🚀",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()

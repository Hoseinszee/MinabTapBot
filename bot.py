import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("TOKEN", "8746114474:AAEis62cyRb-ZsIPal0LgD9D22E9tBVbr9I")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    ref_link = f"https://t.me/MinabTapBot?start={user_id}"
    
    keyboard = [
        [InlineKeyboardButton(
            "🎯 باز کن میناب تسک",
            web_app=WebAppInfo(url="https://jazzy-pixie-6169f8.netlify.app/")
        )],
        [InlineKeyboardButton("🔗 لینک رفرال من", callback_data="reflink")],
    ]
    await update.message.reply_text(
        "🕊️ *میناب تسک*\n\nبه یاد شهدای مدرسه میناب #Minab168\n\nتسک انجام بده و جایزه بگیر! 🎁",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def reflink(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    ref_link = f"https://t.me/MinabTapBot?start={user_id}"
    await query.answer()
    await query.message.reply_text(
        f"🔗 *لینک رفرال تو:*\n\n`{ref_link}`\n\nهر کی از این لینک بیاد +200 امتیاز میگیری!",
        parse_mode="Markdown"
    )

from telegram.ext import CallbackQueryHandler
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(reflink, pattern="reflink"))
app.run_polling()

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes8746114474:AAEvKuUsnZVrlWfi_YdTn_E-zBM9nd1J3Vs
# ←←← اینجا توکن باتت رو بذار ↓↓↓8746114474:AAEvKuUsnZVrlWfi_YdTn_E-zBM9nd1J3Vs
TOKEN = "8746114474:AAEvKuUsnZVrlWfi_YdTn_E-zBM9nd1J3Vs"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 سلام! به بات Tap to Earn خوش اومدی!\n\nبرای گرفتن امتیاز بنویس: /tap")

async def tap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ +۱۰ امتیاز گرفتی!\n\nبالانس فعلی: ۱۰ امتیاز 🎉")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("tap", tap))

print("✅ بات با موفقیت شروع شد!")
app.run_polling()
nano bot.py


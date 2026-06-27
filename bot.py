import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("TOKEN", "8746114474:AAEis62cyRb-ZsIPal0LgD9D22E9tBVbr9I")

users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in users:
        users[user_id] = {"points": 0, "tasks": []}
    keyboard = [
        [InlineKeyboardButton("📋 تسک‌ها", callback_data="tasks")],
        [InlineKeyboardButton("💰 امتیاز من", callback_data="points")],
    ]
    await update.message.reply_text(
        "🎁 به بات ایردراپ خوش اومدی!\nتسک انجام بده و جایزه بگیر!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    if user_id not in users:
        users[user_id] = {"points": 0, "tasks": []}
    
    if query.data == "tasks":
        keyboard = [
            [InlineKeyboardButton("✅ جوین کانال تلگرام", callback_data="task_telegram")],
            [InlineKeyboardButton("✅ فالو تویتر", callback_data="task_twitter")],
            [InlineKeyboardButton("🔙 برگشت", callback_data="back")],
        ]
        await query.edit_message_text("📋 تسک‌ها:", reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif query.data == "task_telegram":
        if "telegram" not in users[user_id]["tasks"]:
            users[user_id]["tasks"].append("telegram")
            users[user_id]["points"] += 100
            await query.edit_message_text("✅ کانال @f1vra رو جوین کن!\n\n+100 امتیاز گرفتی!")
        else:
            await query.edit_message_text("قبلاً این تسک رو انجام دادی!")
    
    elif query.data == "task_twitter":
        if "twitter" not in users[user_id]["tasks"]:
            users[user_id]["tasks"].append("twitter")
            users[user_id]["points"] += 100
            await query.edit_message_text("✅ تویتر @Hoseinsze رو فالو کن!\n\n+100 امتیاز گرفتی!")
        else:
            await query.edit_message_text("قبلاً این تسک رو انجام دادی!")
    
    elif query.data == "points":
        points = users[user_id]["points"]
        await query.edit_message_text(f"💰 امتیاز تو: {points}")
    
    elif query.data == "back":
        keyboard = [
            [InlineKeyboardButton("📋 تسک‌ها", callback_data="tasks")],
            [InlineKeyboardButton("💰 امتیاز من", callback_data="points")],
        ]
        await query.edit_message_text(
            "🎁 به بات ایردراپ خوش اومدی!\nتسک انجام بده و جایزه بگیر!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.run_polling()

import os
import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("TOKEN", "8746114474:AAEis62cyRb-ZsIPal0LgD9D22E9tBVbr9I")
SUPABASE_URL = "https://nrbahixaupzfbbixegwo.supabase.co"
SUPABASE_KEY = "sb_publishable_XLmSYz20ZAEJUd4p7bdG-A_a1gGLsyJ"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

async def get_user(user_id):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{SUPABASE_URL}/rest/v1/users?id=eq.{user_id}", headers=headers)
        data = r.json()
        return data[0] if data else None

async def create_user(user_id, username, referrer_id=None):
    async with httpx.AsyncClient() as client:
        data = {"id": user_id, "username": username}
        if referrer_id:
            data["referrer_id"] = referrer_id
        await client.post(f"{SUPABASE_URL}/rest/v1/users", headers=headers, json=data)

async def add_referral(referrer_id):
    user = await get_user(referrer_id)
    if user:
        async with httpx.AsyncClient() as client:
            await client.patch(
                f"{SUPABASE_URL}/rest/v1/users?id=eq.{referrer_id}",
                headers=headers,
                json={
                    "referral_count": user["referral_count"] + 1,
                    "tokens": user["tokens"] + 5000,
                    "points": user["points"] + 500
                }
            )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    username = user.username or user.first_name

    referrer_id = None
    if context.args:
        try:
            referrer_id = int(context.args[0])
            if referrer_id == user_id:
                referrer_id = None
        except:
            pass

    existing = await get_user(user_id)
    if not existing:
        await create_user(user_id, username, referrer_id)
        if referrer_id:
            await add_referral(referrer_id)
            await context.bot.send_message(
                referrer_id,
                f"🎉 یه نفر از لینک رفرال تو اومد!\n+500 امتیاز و +5000 MINAB168 گرفتی! 🚀"
            )

    ref_link = f"https://t.me/MinabTapBot?start={user_id}"
    keyboa
pip install httpx --break-system-packages
git add bot.py
git commit -m "supabase referral"
git push


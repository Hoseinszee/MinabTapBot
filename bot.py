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

TEXTS = {
    "fa": {
        "welcome": "🕊️ میناب تسک\n\nسلام {name}!\n\nبه یاد شهدای مدرسه میناب\n\nهر دعوت = +5000 MINAB168 و +500 امتیاز!\n\nتسک انجام بده و جایزه بگیر!",
        "open": "🎯 باز کن میناب تسک",
        "reflink": "🔗 لینک رفرال من",
        "stats": "📊 امتیاز من",
        "lang": "🌐 English",
        "ref_msg": "لینک رفرال تو:\n\n{link}\n\nهر دعوت = +5000 MINAB168 و +500 امتیاز!",
        "stats_msg": "آمار تو:\n\nامتیاز: {points}\nMINAB168: {tokens}\nرفرال ها: {refs}\nدرآمد رفرال: {ref_tokens} MINAB168",
        "new_ref": "یه نفر از لینک رفرال تو اومد!\n+500 امتیاز و +5000 MINAB168 گرفتی!",
    },
    "en": {
        "welcome": "🕊️ Minab Task\n\nHello {name}!\n\nIn memory of Minab school martyrs\n\nEach invite = +5000 MINAB168 & +500 points!\n\nComplete tasks and win rewards!",
        "open": "🎯 Open Minab Task",
        "reflink": "🔗 My Referral Link",
        "stats": "📊 My Stats",
        "lang": "🌐 فارسی",
        "ref_msg": "Your referral link:\n\n{link}\n\nEach invite = +5000 MINAB168 & +500 points!",
        "stats_msg": "Your Stats:\n\nPoints: {points}\nMINAB168: {tokens}\nReferrals: {refs}\nReferral earnings: {ref_tokens} MINAB168",
        "new_ref": "Someone joined via your referral link!\n+500 points & +5000 MINAB168 earned!",
    }
}

user_langs = {}

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

def get_keyboard(user_id, lang):
    t = TEXTS[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t["open"], web_app=WebAppInfo(url="https://jazzy-pixie-6169f8.netlify.app/"))],
        [InlineKeyboardButton(t["reflink"], callback_data="reflink"),
         InlineKeyboardButton(t["stats"], callback_data="mystats")],
        [InlineKeyboardButton(t["lang"], callback_data="lang")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    username = user.username or user.first_name
    lang = user_langs.get(user_id, "fa")

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
            ref_lang = user_langs.get(referrer_id, "fa")
            await context.bot.send_message(referrer_id, TEXTS[ref_lang]["new_ref"])

    t = TEXTS[lang]
    await update.message.reply_text(
        t["welcome"].format(name=username),
        reply_markup=get_keyboard(user_id, lang)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    lang = user_langs.get(user_id, "fa")
    await query.answer()

    if query.data == "lang":
        user_langs[user_id] = "en" if lang == "fa" else "fa"
        lang = user_langs[user_id]
        t = TEXTS[lang]
        username = query.from_user.username or query.from_user.first_name
        await query.edit_message_text(
            t["welcome"].format(name=username),
            reply_markup=get_keyboard(user_id, lang)
        )

    elif query.data == "reflink":
        t = TEXTS[lang]
        ref_link = f"https://t.me/MinabTapBot?start={user_id}"
        await query.message.reply_text(t["ref_msg"].format(link=ref_link))

    elif query.data == "mystats":
        t = TEXTS[lang]
        user = await get_user(user_id)
        if user:
            await query.message.reply_text(
                t["stats_msg"].format(
                    points=user["points"],
                    tokens=user["tokens"],
                    refs=user["referral_count"],
                    ref_tokens=user["referral_count"] * 5000
                )
            )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.run_polling()

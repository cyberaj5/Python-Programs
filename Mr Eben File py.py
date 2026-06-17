import os
import threading
import re
import phonenumbers
from flask import Flask
from supabase import create_client, Client
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters, Application
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
0
# Flask setup
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is runnin!!"

# Supabase setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Constants
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
TELEGRAM_GROUP_LINK = "https://t.me/cabvibebetagroup"
PORT = int(os.getenv("PORT", 10000))

# In-memory temp state store
user_states = {}

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    try:
        response = supabase.table("users").select("*").eq("telegram_id", str(user_id)).limit(1).execute()
        if response.data and len(response.data) > 0:
            user = response.data[0]
            keyboard = [[InlineKeyboardButton("🚀 Hop Into the Group!", url=TELEGRAM_GROUP_LINK)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                f"""✅ Hey {user['name']}! You're already good to go. 😎

Welcome back to Cabvibe — where rides meet the metaverse! 🌍🚗""",
                reply_markup=reply_markup
            )
            return
    except Exception as e:
        print("Supabase fetch error:", e)
        await update.message.reply_text("⚠️ Hmm... couldn't check your status. Mind trying again in a bit?")
        return

    keyboard = [
        [InlineKeyboardButton("🟢 Let's Get Verified!", callback_data="start_verification")],
        [
            InlineKeyboardButton("ℹ️ About Us", url="https://cabvibe.com/about-us"),
            InlineKeyboardButton("📞 Support", url="https://cabvibe.com/contact")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        """👋 Hey there! Welcome to **Cabvibe** — the future of ride-hailing, now cruisin' into the metaverse 🚀

Before we get you into the VIP community group, we just need to do a quick and easy verification. Let’s go! 👇""",
        reply_markup=reply_markup
    )

# Handle button callbacks
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == "start_verification":
        user_states[user_id] = {}
        await query.message.reply_text("👤 Cool! First up — what's your full name?")

# Handle user messages (text input)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()

    if user_id not in user_states:
        await start(update, context)
        return

    state = user_states.get(user_id, {})

    if 'name' not in state:
        state['name'] = text
        user_states[user_id] = state
        await update.message.reply_text("📧 Sweet! Now drop your email address:")
        return

    if 'email' not in state:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", text):
            await update.message.reply_text("😅 Hmm... that doesn't look like a proper email. Try again?")
            return
        state['email'] = text
        user_states[user_id] = state
        await update.message.reply_text("📱 Almost done! Send me your phone number (with country code, e.g. +234...)")
        return

    if 'phone' not in state:
        try:
            phone_number = phonenumbers.parse(text, None)
            if not phonenumbers.is_valid_number(phone_number):
                raise ValueError("Invalid number")
            formatted_phone = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)
            state['phone'] = formatted_phone
        except Exception:
            await update.message.reply_text("🚫 That phone number doesn't look right. Make sure to include the country code like +234...")
            return
        
        try:
            data = {
                "telegram_id": str(user_id),
                "name": state["name"],
                "email": state["email"],
                "phone": state["phone"]
            }
            response = supabase.table("users").insert(data).execute()
            if not response.data:
                raise Exception("Insert failed — no data returned.")
        except Exception as e:
            print("Supabase error:", e)
            await update.message.reply_text("⚠️ Oops, something went wrong while saving your details. Give it another shot in a bit.")
            return

        keyboard = [[InlineKeyboardButton("🚀 Hop Into the Group!", url=TELEGRAM_GROUP_LINK)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"""🎉 Awesome stuff, {state['name']}! You're all set and verified. ✅

Welcome aboard Cabvibe — let’s redefine the future of rides together! 🌐💫""",
            reply_markup=reply_markup
        )
        user_states.pop(user_id, None)
        return

# Main entry
if __name__ == '__main__':
    # Start Flask in a thread
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=PORT)).start()

    # Telegram application
    application = ApplicationBuilder().token(TELEGRAM_API_KEY).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print('Bot is Polling...')
    application.run_polling()

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

# Your BotFather token
TOKEN = "7205657511:AAFlt5KaLuWYqzmPXksXjKdI2VpEWTnpbPw"

# Example property data (manual)
properties = {
    "Gbagada": {
      "1_room": {"100k-200k": ["1 Room at Gbagada, ₦150k"]},
      "2_room": {"200k-400k": ["2 Bedroom at Gbagada, ₦350k"]},
    },
    "ikeja": {
        "1_room": {"100k-200k": ["1 Room at Ikeja, ₦150k"]},
        "2_room": {"200k-400k": ["2 Bedroom at Ikeja, ₦350k"]},
    },
    "lekki": {
        "1_room": {"200k-400k": ["1 Room at Lekki, ₦250k"]},
        "2_room": {"400k-600k": ["2 Bedroom at Lekki, ₦500k"]},
    }
}

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Customer Service", callback_data="customer_service")],
        [InlineKeyboardButton("Find Apartment", callback_data="find_apartment")]
    ]
    await update.message.reply_text(
        "👋 Welcome to MyRentEase! Please choose:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Handle button presses
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # Handle Customer Service
    if data == "customer_service":
        await query.edit_message_text("📞 Contact our support at: +234 800 123 4567")

    # Handle Find Apartment
    elif data == "find_apartment":
        # Yes, you can have multiple InlineKeyboardButtons in a single InlineKeyboardMarkup.
        # Each list inside 'keyboard' is a row of buttons.
        keyboard = [
            [InlineKeyboardButton("Gbagada", callback_data="area:Gbagada")],
            [InlineKeyboardButton("Ikeja", callback_data="area:ikeja")],
            [InlineKeyboardButton("Lekki", callback_data="area:lekki")]
        ]
        await query.edit_message_text("🏙️ Choose an area:", reply_markup=InlineKeyboardMarkup(keyboard))

    # Handle Area
    elif data.startswith("area:"):
        area = data.split(":")[1]
        keyboard = [
            [InlineKeyboardButton("1 Room", callback_data=f"rooms:{area}:1_room")],
            [InlineKeyboardButton("2 Room", callback_data=f"rooms:{area}:2_room")]
        ]
        await query.edit_message_text(f"🏠 Choose apartment type in {area.title()}:", reply_markup=InlineKeyboardMarkup(keyboard))

    # Handle Rooms
    elif data.startswith("rooms:"):
        _, area, rooms = data.split(":")
        prices = list(properties[area][rooms].keys())
        keyboard = [
            [InlineKeyboardButton(price, callback_data=f"price:{area}:{rooms}:{price}")]
            for price in prices
        ]
        await query.edit_message_text("💰 Choose price range:", reply_markup=InlineKeyboardMarkup(keyboard))

    # Handle Price Selection
    elif data.startswith("price:"):
        _, area, rooms, price_range = data.split(":", 3)  # allow colons safely
        results = properties[area][rooms].get(price_range, ["No apartments found."])
        await query.edit_message_text("📋 Results:\n" + "\n".join(results))

# Main function
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Customer Service", callback_data="service")],
        [InlineKeyboardButton("Find Apartment", callback_data="find_apartment")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! How can we help you?", reply_markup=reply_markup)

# Handle button clicks
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "find_apartment":
        # Example areas, you should fetch from website dynamically
        keyboard = [
            [InlineKeyboardButton("Lekki", callback_data="area_lekki")],
            [InlineKeyboardButton("Ikeja", callback_data="area_ikeja")],
            [InlineKeyboardButton("Yaba", callback_data="area_yaba")]
        ]
        await query.edit_message_text("Select location:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith("area_"):
        area = query.data.split("_")[1]
        context.user_data["area"] = area
        keyboard = [
            [InlineKeyboardButton("1 Bedroom", callback_data="bed_1")],
            [InlineKeyboardButton("2 Bedroom", callback_data="bed_2")],
            [InlineKeyboardButton("3 Bedroom", callback_data="bed_3")]
        ]
        await query.edit_message_text(f"You selected {area}. How many bedrooms?", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith("bed_"):
        bedrooms = query.data.split("_")[1]
        context.user_data["bedrooms"] = bedrooms
        # Now ask for price range
        keyboard = [
            [InlineKeyboardButton("₦200k - ₦500k", callback_data="price_200_500")],
            [InlineKeyboardButton("₦500k - ₦1M", callback_data="price_500_1000")],
            [InlineKeyboardButton("₦1M+", callback_data="price_1000_plus")]
        ]
        await query.edit_message_text(f"Selected {bedrooms} bedroom(s). Choose price range:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith("price_"):
        price_range = query.data.split("_")[1:]
        context.user_data["price"] = price_range
        area = context.user_data.get("area")
        bedrooms = context.user_data.get("bedrooms")

        # Here, fetch results from site or database
        listings = get_listings(area, bedrooms, price_range)  # integrate scraper/API
        if listings:
            reply_text = "Here are some options:\n\n"
            for l in listings[:5]:  # show first 5
                reply_text += f"{l['title']} - {l['price']}\n{l['link']}\n\n"
        else:
            reply_text = "Sorry, no apartments found."

        await query.edit_message_text(reply_text)

def main():
    app = Application.builder().token("7205657511:AAFlt5KaLuWYqzmPXksXjKdI2VpEWTnpbPw").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()

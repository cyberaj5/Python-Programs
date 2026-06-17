import logging
import sqlite3
from telegram import (
    Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
)
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters,
    ConversationHandler, ContextTypes, CallbackQueryHandler
)
from typing import Final
token: Final = "8484660494:AAGvtI49sHFMbuOHTrg4UedmsG1DfuJ0etc"
Bot_username: Final = "@campuslink_bot"
# Add a command handler for /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Start the bot and show main menu\n"
        "/help - Show this help message\n"
        "Or use the menu buttons to buy, sell, or view listings."
    )
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

DB_FILE = 'market.db'

def init_db():
    """Initialize the SQLite database and create items table if not exists."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            seller_id INTEGER,
            seller_name TEXT,
            item_name TEXT,
            description TEXT,
            price REAL,
            location TEXT,
            contact TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Conversation states
(
    MAIN_MENU,
    SELL_ITEM_NAME,
    SELL_ITEM_DESC,
    SELL_ITEM_PRICE,
    SELL_ITEM_LOCATION,
    SELL_ITEM_CONTACT,
    SEARCH_KEYWORD,
    SEARCH_PRICE,
    SEARCH_LOCATION,
    VIEW_LISTINGS,
    CONFIRM_DELETE
) = range(11)

# Keyboards
main_menu_keyboard = [
    ["🛒 Buy an Item", "📦 Sell an Item"],
    ["📋 View My Listings", "🔍 Search Again"],
    ["🔙 Back to Main Menu"]
]
main_menu_markup = ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)

def add_item(seller_id, seller_name, item_name, description, price, location, contact):
    """Add a new item to the database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO items (seller_id, seller_name, item_name, description, price, location, contact)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (seller_id, seller_name, item_name, description, price, location, contact))
    conn.commit()
    conn.close()

def search_items(keyword, min_price=None, max_price=None, location=None):
    """Search items by keyword, price range, and location."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    query = "SELECT item_id, item_name, description, price, location, contact, seller_name FROM items WHERE item_name LIKE ? OR description LIKE ?"
    params = [f"%{keyword}%", f"%{keyword}%"]
    if min_price is not None:
        query += " AND price >= ?"
        params.append(min_price)
    if max_price is not None:
        query += " AND price <= ?"
        params.append(max_price)
    if location:
        query += " AND location LIKE ?"
        params.append(f"%{location}%")
    c.execute(query, params)
    results = c.fetchall()
    conn.close()
    return results

def get_user_listings(seller_id):
    """Get all listings for a seller."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT item_id, item_name, price, location FROM items WHERE seller_id=?", (seller_id,))
    listings = c.fetchall()
    conn.close()
    return listings

def delete_listing(item_id, seller_id):
    """Delete a listing by item_id and seller_id."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM items WHERE item_id=? AND seller_id=?", (item_id, seller_id))
    conn.commit()
    conn.close()

# --- Conversation Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message and show main menu."""
    await update.message.reply_text(
        "Welcome to Xceptional Market!\nBuy and sell items with fellow ESTAM students.",
        reply_markup=main_menu_markup
    )
    return MAIN_MENU

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle main menu selection."""
    text = update.message.text
    if text == "📦 Sell an Item":
        await update.message.reply_text("Enter the item name:", reply_markup=ReplyKeyboardRemove())
        return SELL_ITEM_NAME
    elif text == "🛒 Buy an Item":
        await update.message.reply_text("Enter a keyword to search for items:", reply_markup=ReplyKeyboardRemove())
        return SEARCH_KEYWORD
    elif text == "📋 View My Listings":
        listings = get_user_listings(update.message.from_user.id)
        if not listings:
            await update.message.reply_text("You have no listings.", reply_markup=main_menu_markup)
            return MAIN_MENU
        msg = "Your Listings:\n"
        buttons = []
        for item_id, name, price, location in listings:
            msg += f"\nID: {item_id}\nName: {name}\nPrice: {price}\nLocation: {location}\n"
            buttons.append([InlineKeyboardButton(f"Delete {name}", callback_data=f"del_{item_id}")])
        await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(buttons))
        return VIEW_LISTINGS
    elif text == "🔍 Search Again":
        await update.message.reply_text("Enter a keyword to search for items:", reply_markup=ReplyKeyboardRemove())
        return SEARCH_KEYWORD
    elif text == "🔙 Back to Main Menu":
        await update.message.reply_text("Back to main menu.", reply_markup=main_menu_markup)
        return MAIN_MENU
    else:
        await update.message.reply_text("Please choose an option from the menu.", reply_markup=main_menu_markup)
        return MAIN_MENU

# --- Sell Item Flow ---
async def sell_item_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['item_name'] = update.message.text
    await update.message.reply_text("Enter a description for your item:")
    return SELL_ITEM_DESC

async def sell_item_desc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['description'] = update.message.text
    await update.message.reply_text("Enter the price (numbers only):")
    return SELL_ITEM_PRICE

async def sell_item_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        price = float(update.message.text)
        context.user_data['price'] = price
    except ValueError:
        await update.message.reply_text("Invalid price. Please enter a number:")
        return SELL_ITEM_PRICE
    await update.message.reply_text("Enter the location:")
    return SELL_ITEM_LOCATION

async def sell_item_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['location'] = update.message.text
    await update.message.reply_text("Enter your contact info (phone/email):")
    return SELL_ITEM_CONTACT

async def sell_item_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    add_item(
        seller_id=user.id,
        seller_name=user.full_name,
        item_name=context.user_data['item_name'],
        description=context.user_data['description'],
        price=context.user_data['price'],
        location=context.user_data['location'],
        contact=update.message.text
    )
    await update.message.reply_text("Your item has been listed!", reply_markup=main_menu_markup)
    return MAIN_MENU

# --- Search Flow ---
async def search_keyword(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['search_keyword'] = update.message.text
    await update.message.reply_text("Enter minimum price (or type 'skip'):")
    return SEARCH_PRICE

async def search_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text.lower() == 'skip':
        context.user_data['min_price'] = None
    else:
        try:
            context.user_data['min_price'] = float(text)
        except ValueError:
            await update.message.reply_text("Invalid price. Please enter a number or type 'skip':")
            return SEARCH_PRICE
    await update.message.reply_text("Enter location (or type 'skip'):")
    return SEARCH_LOCATION

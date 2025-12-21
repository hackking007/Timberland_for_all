import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import json

TOKEN = os.environ.get("TELEGRAM_TOKEN")
USER_DATA_FILE = "data/user_data.json"

def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {"users": {}}

def save_user_data(data):
    os.makedirs(os.path.dirname(USER_DATA_FILE), exist_ok=True)
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👨 Men", callback_data="cat_men")],
        [InlineKeyboardButton("👩 Women", callback_data="cat_women")],
        [InlineKeyboardButton("👶 Kids", callback_data="cat_kids")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Select category:", reply_markup=reply_markup)

async def category_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    category = query.data.replace("cat_", "")
    user_id = str(query.from_user.id)
    
    # Save category
    data = load_user_data()
    if user_id not in data["users"]:
        data["users"][user_id] = {}
    data["users"][user_id]["category"] = category
    save_user_data(data)
    
    # Show size selection based on category
    if category == "men":
        sizes = ["40", "40.5", "41", "41.5", "42", "42.5", "43", "43.5", "44", "44.5", "45", "45.5", "46", "46.5", "47", "47.5"]
    elif category == "women":
        sizes = ["35.5", "36", "36.5", "37", "37.5", "38", "38.5", "39", "39.5", "40", "40.5", "41"]
    else:  # kids
        sizes = ["28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40"]
    
    # Create keyboard with sizes (max 3 per row)
    keyboard = []
    for i in range(0, len(sizes), 3):
        row = [InlineKeyboardButton(size, callback_data=f"size_{size}") for size in sizes[i:i+3]]
        keyboard.append(row)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f"Select size for {category}:", reply_markup=reply_markup)

async def size_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    size = query.data.replace("size_", "")
    user_id = str(query.from_user.id)
    
    # Save size
    data = load_user_data()
    data["users"][user_id]["size"] = size
    save_user_data(data)
    
    # Show price selection
    keyboard = [
        [InlineKeyboardButton("₪10-299", callback_data="price_10_299")],
        [InlineKeyboardButton("₪10-499", callback_data="price_10_499")],
        [InlineKeyboardButton("₪10-999", callback_data="price_10_999")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f"Size {size} selected. Choose price range:", reply_markup=reply_markup)

async def price_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    price_range = query.data.replace("price_", "")
    price_min, price_max = price_range.split("_")
    user_id = str(query.from_user.id)
    
    # Save price and complete setup
    data = load_user_data()
    data["users"][user_id]["price_min"] = int(price_min)
    data["users"][user_id]["price_max"] = int(price_max)
    data["users"][user_id]["onboarding_state"] = "COMPLETED"
    data["users"][user_id]["active"] = True
    
    # Generate URL
    user_data = data["users"][user_id]
    url = f"https://www.timberland.co.il/search?gender={user_data['category']}&size={user_data['size']}&price={price_min}_{price_max}"
    data["users"][user_id]["generated_url"] = url
    
    save_user_data(data)
    
    await query.edit_message_text(
        f"✅ Setup complete!\n"
        f"Category: {user_data['category']}\n"
        f"Size: {user_data['size']}\n"
        f"Price: ₪{price_min}-{price_max}\n\n"
        f"URL: {url}"
    )

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(category_callback, pattern="^cat_"))
    app.add_handler(CallbackQueryHandler(size_callback, pattern="^size_"))
    app.add_handler(CallbackQueryHandler(price_callback, pattern="^price_"))
    
    print("Bot started! Send /start in Telegram")
    app.run_polling()

if __name__ == "__main__":
    main()

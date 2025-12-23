import json
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import asyncio

# Import your bot modules
import sys
sys.path.append('./bot')
from simple_bot import start, category_callback, size_callback, price_callback

TOKEN = os.environ.get("TELEGRAM_TOKEN")

async def handler(request):
    if request.method == "POST":
        # Handle Telegram webhook
        update_data = await request.json()
        update = Update.de_json(update_data, None)
        
        # Create application
        app = Application.builder().token(TOKEN).build()
        
        # Add handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(category_callback, pattern="^cat_"))
        app.add_handler(CallbackQueryHandler(size_callback, pattern="^size_"))
        app.add_handler(CallbackQueryHandler(price_callback, pattern="^price_"))
        
        # Process update
        await app.process_update(update)
        
        return {"statusCode": 200}
    
    return {"statusCode": 200, "body": "Bot is running"}

# Vercel entry point
def lambda_handler(event, context):
    return asyncio.run(handler(event))

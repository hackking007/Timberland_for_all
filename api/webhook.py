import json
import os
import sys
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import asyncio

# Import your bot modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from bot.simple_bot import start, category_callback, size_callback, price_callback

TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Create Flask app
app = Flask(__name__)

# Create bot application (reuse across requests)
bot_app = None

def get_bot_app():
    global bot_app
    if bot_app is None:
        bot_app = Application.builder().token(TOKEN).build()
        
        # Add handlers
        bot_app.add_handler(CommandHandler("start", start))
        bot_app.add_handler(CallbackQueryHandler(category_callback, pattern="^cat_"))
        bot_app.add_handler(CallbackQueryHandler(size_callback, pattern="^size_"))
        bot_app.add_handler(CallbackQueryHandler(price_callback, pattern="^price_"))
        
        # Initialize the application
        asyncio.get_event_loop().run_until_complete(bot_app.initialize())
    
    return bot_app

@app.route('/api/webhook', methods=['POST', 'GET'])
def webhook():
    if request.method == 'GET':
        return jsonify({"status": "Bot is running", "ok": True})
    
    try:
        # Get update data
        update_data = request.get_json(force=True)
        print(f"Received update: {update_data}")  # Debug log
        
        # Create Update object
        application = get_bot_app()
        update = Update.de_json(update_data, application.bot)
        
        # Process update with proper event loop handling
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(application.process_update(update))
        finally:
            loop.close()
        
        return jsonify({"ok": True})
    
    except Exception as e:
        print(f"Error processing update: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"ok": False, "error": str(e)}), 500

# For Vercel serverless
def handler(environ, start_response):
    return app(environ, start_response)

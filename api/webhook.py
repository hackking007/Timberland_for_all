import os
import sys
import asyncio
from flask import Flask, request, jsonify

app = Flask(__name__)

async def run_bot_logic(update_data):
    # Lazy import to avoid Vercel loading issues at top level
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from bot.telegram_bot import TelegramBot
    
    # Initialize the bot instance (connects to Mongo, sets up handlers)
    bot_instance = TelegramBot()
    telegram_app = bot_instance.app
    
    # Process the update
    await telegram_app.initialize()
    await telegram_app.process_update(Update.de_json(update_data, telegram_app.bot))
    await telegram_app.shutdown()

@app.route('/api/webhook', methods=['POST', 'GET'])
def webhook_handler():
    if request.method == 'GET':
        return "Bot is running!", 200
    
    try:
        from telegram import Update # Import Update here too if needed or keep top level if safe
        
        update_data = request.get_json()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_bot_logic(update_data))
        loop.close()
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Vercel handler - explicitly set
handler = app

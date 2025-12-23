import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from functools import lru_cache

# Import your handlers
from bot.simple_bot import start, category_callback, size_callback, price_callback

TOKEN = os.environ.get("TELEGRAM_TOKEN")

@lru_cache()
def get_bot_app():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(category_callback, pattern="^cat_"))
    app.add_handler(CallbackQueryHandler(size_callback, pattern="^size_"))
    app.add_handler(CallbackQueryHandler(price_callback, pattern="^price_"))
    return app

def handler(request):
    """
    Vercel Python function entrypoint.
    It must accept a request and return a body & status.
    """
    # Verify it's POST
    if request.method != "POST":
        return {
            "statusCode": 200,
            "body": "OK – send POST from Telegram only"
        }

    try:
        update_data = request.get_json()

        app = get_bot_app()

        # Convert to Update
        update = Update.de_json(update_data, app.bot)

        # Process update
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(app.process_update(update))
        loop.close()

        return {"statusCode": 200, "body": "OK"}
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }

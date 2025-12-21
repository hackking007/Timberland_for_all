import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, 
    ContextTypes
)
from config import TELEGRAM_TOKEN
from user_store import UserStore
from onboarding import OnboardingManager
from scraper import Scraper

class TelegramBot:
    def __init__(self):
        self.user_store = UserStore()
        self.onboarding = OnboardingManager(self.user_store)
        self.app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        self._setup_handlers()
    
    def _setup_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("settings", self.settings_command))
        self.app.add_handler(CommandHandler("myurl", self.myurl_command))
        self.app.add_handler(CommandHandler("test", self.test_command))
        
        # Callback handlers for inline keyboards
        self.app.add_handler(CallbackQueryHandler(
            self.onboarding.handle_category_selection, 
            pattern="^cat_"
        ))
        self.app.add_handler(CallbackQueryHandler(
            self.onboarding.handle_size_selection, 
            pattern="^size_"
        ))
        self.app.add_handler(CallbackQueryHandler(
            self.onboarding.handle_price_selection, 
            pattern="^price_"
        ))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.onboarding.start_onboarding(update, context)
    
    async def settings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = str(update.effective_user.id)
        user = self.user_store.get_user(user_id)
        
        if not user:
            await update.message.reply_text("Please use /start first to set up your preferences.")
            return
        
        filters = user.get("filters", {})
        url = user.get("generated_url", "Not generated")
        
        await update.message.reply_text(
            f"Current Settings:\n"
            f"Category: {filters.get('category', 'Not set')}\n"
            f"Size: {filters.get('size_label', 'Not set')}\n"
            f"Price Range: {filters.get('price_min', 0)}-{filters.get('price_max', 0)}\n\n"
            f"Generated URL: {url}\n\n"
            f"To modify settings, use /start"
        )
    
    async def myurl_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = str(update.effective_user.id)
        user = self.user_store.get_user(user_id)
        
        if not user or not user.get("generated_url"):
            await update.message.reply_text("No URL generated. Please use /start to set up your preferences.")
            return
        
        await update.message.reply_text(f"Your tracking URL:\n{user['generated_url']}")
    
    async def test_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = str(update.effective_user.id)
        user = self.user_store.get_user(user_id)
        
        if not user or not user.get("generated_url"):
            await update.message.reply_text("No URL to test. Please use /start first.")
            return
        
        await update.message.reply_text("Testing your URL... Please wait.")
        
        try:
            products = Scraper.fetch_products(user["generated_url"])
            
            if not products:
                await update.message.reply_text("No products found with your current filters.")
                return
            
            # Show first 3 products
            message_parts = [f"Found {len(products)} products. Here are the first 3:\n"]
            
            for i, product in enumerate(products[:3], 1):
                message_parts.append(
                    f"{i}. {product['title']}\n"
                    f"   Price: ₪{product['price']}\n"
                    f"   URL: {product['url']}\n"
                )
            
            await update.message.reply_text("\n".join(message_parts))
            
        except Exception as e:
            await update.message.reply_text(f"Error testing URL: {str(e)}")
    
    def run(self):
        print("Starting Telegram bot...")
        self.app.run_polling()

if __name__ == "__main__":
    bot = TelegramBot()
    bot.run()
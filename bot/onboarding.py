import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from user_store import UserStore
from url_builder import URLBuilder
from config import OnboardingState, SIZE_MAP_FILE

class OnboardingManager:
    def __init__(self, user_store: UserStore):
        self.user_store = user_store
        self.size_map = self._load_size_map()
    
    def _load_size_map(self):
        if os.path.exists(SIZE_MAP_FILE):
            with open(SIZE_MAP_FILE, 'r') as f:
                return json.load(f)
        return {}
    
    async def start_onboarding(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = str(update.effective_user.id)
        user = self.user_store.get_user(user_id)
        
        if not user:
            user = self.user_store.create_user(user_id)
        
        if user["onboarding_state"] == OnboardingState.COMPLETED:
            await self._show_current_config(update, user)
            return
        
        self.user_store.update_user(user_id, {"onboarding_state": OnboardingState.SELECT_CATEGORY})
        await self._show_category_selection(update)
    
    async def _show_category_selection(self, update: Update):
        keyboard = [
            [InlineKeyboardButton("👨 Men", callback_data="cat_men")],
            [InlineKeyboardButton("👩 Women", callback_data="cat_women")],
            [InlineKeyboardButton("👶 Kids", callback_data="cat_kids")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Select category:", reply_markup=reply_markup)
    
    async def handle_category_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        user_id = str(query.from_user.id)
        category = query.data.replace("cat_", "")
        
        self.user_store.update_user(user_id, {
            "filters": {"category": category},
            "onboarding_state": OnboardingState.SELECT_SIZE
        })
        
        await query.answer()
        await self._show_size_selection(query, category)
    
    async def _show_size_selection(self, query, category):
        sizes = self.size_map.get(category, {})
        keyboard = []
        
        for size_label in sorted(sizes.keys(), key=int):
            keyboard.append([InlineKeyboardButton(size_label, callback_data=f"size_{size_label}")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Select size:", reply_markup=reply_markup)
    
    async def handle_size_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        user_id = str(query.from_user.id)
        size_label = query.data.replace("size_", "")
        
        user = self.user_store.get_user(user_id)
        category = user["filters"]["category"]
        size_code = str(self.size_map.get(category, {}).get(size_label, ""))
        
        filters = user["filters"]
        filters.update({"size_label": size_label, "size_code": size_code})
        
        self.user_store.update_user(user_id, {
            "filters": filters,
            "onboarding_state": OnboardingState.SELECT_PRICE
        })
        
        await query.answer()
        await self._show_price_selection(query)
    
    async def _show_price_selection(self, query):
        keyboard = [
            [InlineKeyboardButton("0-100", callback_data="price_0_100")],
            [InlineKeyboardButton("100-200", callback_data="price_100_200")],
            [InlineKeyboardButton("200-300", callback_data="price_200_300")],
            [InlineKeyboardButton("300+", callback_data="price_300_999")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Select price range:", reply_markup=reply_markup)
    
    async def handle_price_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        user_id = str(query.from_user.id)
        price_data = query.data.replace("price_", "").split("_")
        price_min, price_max = int(price_data[0]), int(price_data[1])
        
        user = self.user_store.get_user(user_id)
        filters = user["filters"]
        filters.update({"price_min": price_min, "price_max": price_max})
        
        # Generate URL
        url = URLBuilder.build_url(
            filters["category"], 
            filters["size_code"], 
            price_min, 
            price_max
        )
        
        self.user_store.update_user(user_id, {
            "filters": filters,
            "generated_url": url,
            "onboarding_state": OnboardingState.COMPLETED
        })
        
        await query.answer()
        await query.edit_message_text(
            f"✅ Setup complete!\n"
            f"Category: {filters['category']}\n"
            f"Size: {filters['size_label']}\n"
            f"Price: {price_min}-{price_max}\n\n"
            f"URL: {url}"
        )
    
    async def _show_current_config(self, update: Update, user):
        filters = user["filters"]
        await update.message.reply_text(
            f"Current configuration:\n"
            f"Category: {filters.get('category', 'Not set')}\n"
            f"Size: {filters.get('size_label', 'Not set')}\n"
            f"Price: {filters.get('price_min', 0)}-{filters.get('price_max', 0)}\n\n"
            f"URL: {user.get('generated_url', 'Not generated')}\n\n"
            f"Use /settings to modify"
        )
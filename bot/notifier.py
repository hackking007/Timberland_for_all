import asyncio
from telegram import Bot
from typing import List, Dict
from config import TELEGRAM_TOKEN, EventType

class Notifier:
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_TOKEN)
    
    async def send_notifications(self, user_id: str, events: List[Dict]):
        if not events:
            return
        
        # Send header message
        header = f"🔔 <b>Found {len(events)} Products!</b>\n"
        await self.bot.send_message(chat_id=user_id, text=header, parse_mode='HTML')
        
        # Send each product with photo
        for event in events:
            try:
                await self._send_product_with_photo(user_id, event)
            except Exception as e:
                print(f"Error sending product photo: {e}")
                # Fallback to text message
                message = self._format_single_product(event)
                await self.bot.send_message(chat_id=user_id, text=message, parse_mode='HTML')
    
    async def _send_product_with_photo(self, user_id: str, event: Dict):
        product = event["product"]
        
        if event["type"] == EventType.NEW_PRODUCT:
            caption = (
                f"🆕 <b>New Product</b>\n"
                f"📦 {product['title']}\n"
                f"💰 ₪{product['price']}\n"
                f"🔗 <a href='{product['url']}'>View Product</a>"
            )
        elif event["type"] == EventType.PRICE_DROP:
            old_price = event["old_price"]
            new_price = event["new_price"]
            savings = old_price - new_price
            caption = (
                f"📉 <b>Price Drop</b>\n"
                f"📦 {product['title']}\n"
                f"💰 ₪{old_price} → ₪{new_price} (Save ₪{savings})\n"
                f"🔗 <a href='{product['url']}'>View Product</a>"
            )
        
        if product.get('image'):
            await self.bot.send_photo(
                chat_id=user_id,
                photo=product['image'],
                caption=caption,
                parse_mode='HTML'
            )
        else:
            await self.bot.send_message(
                chat_id=user_id,
                text=caption,
                parse_mode='HTML'
            )
    
    def _format_single_product(self, event: Dict) -> str:
        product = event["product"]
        
        if event["type"] == EventType.NEW_PRODUCT:
            return (
                f"🆕 <b>New Product</b>\n"
                f"📦 {product['title']}\n"
                f"💰 ₪{product['price']}\n"
                f"🔗 <a href='{product['url']}'>View Product</a>"
            )
        elif event["type"] == EventType.PRICE_DROP:
            old_price = event["old_price"]
            new_price = event["new_price"]
            savings = old_price - new_price
            return (
                f"📉 <b>Price Drop</b>\n"
                f"📦 {product['title']}\n"
                f"💰 ₪{old_price} → ₪{new_price} (Save ₪{savings})\n"
                f"🔗 <a href='{product['url']}'>View Product</a>"
            )
    
    async def send_coupons(self, user_id: str, coupons: List[Dict]):
        if not coupons:
            return
        
        try:
            message_parts = ["🎫 <b>Timberland Coupon Codes</b>\n"]
            
            for i, coupon in enumerate(coupons, 1):
                message_parts.append(
                    f"{i}. 🏷️ <code>{coupon['code']}</code>\n"
                    f"   📝 {coupon['description']}\n"
                    f"   📍 Source: {coupon['source']}\n"
                )
            
            message_parts.append("\n📝 Copy the code and paste at checkout!")
            message = "\n".join(message_parts)
            await self.bot.send_message(chat_id=user_id, text=message, parse_mode='HTML')
            
        except Exception as e:
            print(f"Error sending coupons to {user_id}: {e}")

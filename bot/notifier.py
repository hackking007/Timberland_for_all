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
        
        message = self._format_message(events)
        
        try:
            await self.bot.send_message(chat_id=user_id, text=message, parse_mode='HTML')
        except Exception as e:
            print(f"Error sending notification to {user_id}: {e}")
    
    def _format_message(self, events: List[Dict]) -> str:
        message_parts = ["🔔 <b>Product Updates</b>\n"]
        
        for event in events:
            product = event["product"]
            
            if event["type"] == EventType.NEW_PRODUCT:
                message_parts.append(
                    f"🆕 <b>New Product</b>\n"
                    f"📦 {product['title']}\n"
                    f"💰 ₪{product['price']}\n"
                    f"🔗 <a href='{product['url']}'>View Product</a>\n"
                )
            
            elif event["type"] == EventType.PRICE_DROP:
                old_price = event["old_price"]
                new_price = event["new_price"]
                savings = old_price - new_price
                
                message_parts.append(
                    f"📉 <b>Price Drop</b>\n"
                    f"📦 {product['title']}\n"
                    f"💰 ₪{old_price} → ₪{new_price} (Save ₪{savings})\n"
                    f"🔗 <a href='{product['url']}'>View Product</a>\n"
                )
            
            message_parts.append("")  # Empty line between products
        
        return "\n".join(message_parts)
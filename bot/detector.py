from typing import List, Dict
from datetime import datetime
from config import EventType

class ChangeDetector:
    @staticmethod
    def detect_changes(seen_products: Dict, new_products: List[Dict]) -> List[Dict]:
        events = []
        new_product_ids = {p["id"] for p in new_products}
        
        for product in new_products:
            product_id = product["id"]
            
            if product_id not in seen_products:
                # New product
                events.append({
                    "type": EventType.NEW_PRODUCT,
                    "product": product
                })
            else:
                # Check for price drop
                old_price = seen_products[product_id].get("price", 0)
                new_price = product["price"]
                
                if new_price < old_price:
                    events.append({
                        "type": EventType.PRICE_DROP,
                        "product": product,
                        "old_price": old_price,
                        "new_price": new_price
                    })
        
        return events
    
    @staticmethod
    def update_seen_products(seen_products: Dict, new_products: List[Dict], 
                            price_history: Dict) -> tuple:
        timestamp = datetime.now().isoformat()
        
        for product in new_products:
            product_id = product["id"]
            price = product["price"]
            
            # Update seen products
            seen_products[product_id] = {
                "price": price,
                "last_seen": timestamp
            }
            
            # Update price history
            if product_id not in price_history:
                price_history[product_id] = []
            
            price_history[product_id].append([timestamp, price])
            
            # Keep only last 30 entries
            if len(price_history[product_id]) > 30:
                price_history[product_id] = price_history[product_id][-30:]
        
        return seen_products, price_history
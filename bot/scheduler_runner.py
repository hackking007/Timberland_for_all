import asyncio
from config import TELEGRAM_TOKEN
from user_store import UserStore
from scraper import Scraper
from detector import ChangeDetector
from notifier import Notifier

async def run_scan():
    print("Starting scheduled scan...")
    
    # Check if token exists
    if not TELEGRAM_TOKEN:
        print("ERROR: TELEGRAM_TOKEN not found in environment variables")
        print("Please add TELEGRAM_TOKEN to GitHub Secrets")
        return
    
    user_store = UserStore()
    notifier = Notifier()
    
    active_users = user_store.get_all_active_users()
    print(f"Found {len(active_users)} active users")
    
    for user_id, user_data in active_users.items():
        try:
            print(f"Processing user {user_id}...")
            
            url = user_data.get("generated_url")
            if not url:
                print(f"No URL for user {user_id}, skipping")
                continue
            
            # Fetch products
            products = Scraper.fetch_products(url)
            print(f"Fetched {len(products)} products for user {user_id}")
            
            if not products:
                continue
            
            # Detect changes
            seen_products = user_data.get("seen_products", {})
            events = ChangeDetector.detect_changes(seen_products, products)
            print(f"Detected {len(events)} events for user {user_id}")
            
            # Send notifications
            if events:
                await notifier.send_notifications(user_id, events)
            
            # Update state
            seen_products, price_history = ChangeDetector.update_seen_products(
                seen_products, 
                products, 
                user_data.get("price_history", {})
            )
            
            user_store.update_user(user_id, {
                "seen_products": seen_products,
                "price_history": price_history
            })
            
        except Exception as e:
            print(f"Error processing user {user_id}: {e}")
            continue
    
    print("Scan completed")

if __name__ == "__main__":
    asyncio.run(run_scan())

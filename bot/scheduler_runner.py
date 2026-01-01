import asyncio
from config import TELEGRAM_TOKEN
from user_store import UserStore
from scraper import Scraper
from detector import ChangeDetector
from notifier import Notifier
from coupon_scraper import CouponScraper

async def run_scan():
    print("Starting scheduled scan...")
    
    # Check if token exists
    if not TELEGRAM_TOKEN:
        print("ERROR: TELEGRAM_TOKEN not found in environment variables")
        print("Please add TELEGRAM_TOKEN to GitHub Secrets")
        return
    
    user_store = UserStore()
    print(f"Loaded user store with {len(user_store.data.get('users', {}))} total users")
    
    active_users = {uid: data for uid, data in user_store.data["users"].items() 
                    if data.get("active", False) and data.get("onboarding_state") == "COMPLETED"}
    print(f"Found {len(active_users)} active users")
    
    # Debug: print user data
    for uid, data in user_store.data.get("users", {}).items():
        print(f"User {uid}: active={data.get('active')}, state={data.get('onboarding_state')}")
    
    if not active_users:
        print("No active users found, exiting")
        return
    
    notifier = Notifier()
    
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
            
            # Send coupons (always, regardless of products)
            coupons = CouponScraper.fetch_coupons()
            if coupons:
                await notifier.send_coupons(user_id, coupons)
            
            # Update state
            seen_products = user_data.get("seen_products", {})
            price_history = user_data.get("price_history", {})
            
            seen_products, price_history = ChangeDetector.update_seen_products(
                seen_products, 
                products, 
                price_history
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

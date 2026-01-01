from flask import Flask, jsonify
import sys
import os

# Add bot directory to path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'bot'))

from user_store import UserStore
from scraper import Scraper
from detector import ChangeDetector
from notifier import Notifier
from config import TELEGRAM_TOKEN

app = Flask(__name__)

@app.route('/api/cron')
def cron_job():
    try:
        store = UserStore()
        # Fetch all active users who have completed onboarding
        users = store.users.find({
            "active": True,
            "onboarding_state": "COMPLETED",
            "generated_url": {"$ne": None}
        })
        
        results = []
        
        for user in users:
            try:
                user_id = user['user_id']
                url = user['generated_url']
                
                # 1. Scrape
                scraper = Scraper()
                current_products = scraper.scrape(url)
                
                if current_products:
                    # 2. Detect changes
                    detector = ChangeDetector(store)
                    new_items, price_drops = detector.detect_changes(user_id, current_products)
                    
                    # 3. Notify if there are updates
                    if new_items or price_drops:
                        notifier = Notifier(TELEGRAM_TOKEN)
                        # We need to run async function in sync context or manage loop
                        # For simplicity in Vercel serverless (which might be sync), 
                        # we assume notifier has a sync method or we run it:
                        import asyncio
                        asyncio.run(notifier.send_updates(user_id, new_items, price_drops))
                        
                        results.append(f"User {user_id}: Sent {len(new_items)} new, {len(price_drops)} drops")
                    else:
                        results.append(f"User {user_id}: No changes")
                else:
                    results.append(f"User {user_id}: Scrape failed or empty")
                    
            except Exception as e:
                results.append(f"User {user['user_id']} Error: {str(e)}")
                print(f"Error processing user {user.get('user_id')}: {e}")
                
        return jsonify({"status": "success", "results": results}), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Vercel requires the app to be exposed mainly as 'app' or handler
# In some Vercel python runtimes, it looks for 'handler' or 'app'

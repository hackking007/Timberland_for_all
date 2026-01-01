import os
from pymongo import MongoClient

class UserStore:
    def __init__(self):
        # שימוש בכתובת ששלחת - וודא שהחלפת את הכוכביות בסיסמה האמיתית ב-Vercel!
        self.uri = os.environ.get("MONGODB_URI")
        if not self.uri:
            raise ValueError("MONGODB_URI is missing!")
            
        self.client = MongoClient(self.uri)
        # יצירת/חיבור לדאטה-בייס בשם 'timberland_bot'
        self.db = self.client['timberland_bot']
        self.users = self.db['users']

    def save_user(self, user_id, username, first_name):
        user_data = {
            "user_id": user_id,
            "username": username,
            "first_name": first_name
        }
        # שמירה או עדכון של המשתמש
        self.users.update_one({"user_id": user_id}, {"$set": user_data}, upsert=True)
        print(f"User {user_id} saved to MongoDB")

    def create_user(self, user_id):
        """Creates a new user document if it doesn't exist."""
        user_data = {
            "user_id": user_id,
            "onboarding_state": "START",  # Initial state
            "active": True,
            "filters": {},
            "generated_url": None,
            "seen_products": {},
            "price_history": {}
        }
        # In MongoDB, upsert=True with $setOnInsert is often used for "create if not exists",
        # but here we can just use update_one with $setOnInsert to strictly avoid overwriting if exists,
        # or just find_one check before.
        # Let's use logic similar to save_user but solely for initialization.
        
        # Check if exists first to avoid overwriting ongoing progress if called redundantly
        if not self.users.find_one({"user_id": user_id}):
            self.users.insert_one(user_data)
            print(f"New user {user_id} created in MongoDB")
            return user_data
        return self.get_user(user_id)

    def update_user(self, user_id, data):
        """Updates user fields. Supports partial updates."""
        self.users.update_one({"user_id": user_id}, {"$set": data})
        print(f"User {user_id} updated with {data.keys()}")

    def get_user(self, user_id):
        return self.users.find_one({"user_id": user_id})

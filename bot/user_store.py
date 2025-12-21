import json
import os
from typing import Dict, Any, Optional
from config import USER_DATA_FILE

class UserStore:
    def __init__(self):
        self.data = self._load_data()
    
    def _load_data(self) -> Dict[str, Any]:
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"users": {}}
    
    def save_data(self):
        os.makedirs(os.path.dirname(USER_DATA_FILE), exist_ok=True)
        with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.data["users"].get(user_id)
    
    def create_user(self, user_id: str) -> Dict[str, Any]:
        user_data = {
            "onboarding_state": "NOT_STARTED",
            "active": True,
            "filters": {},
            "generated_url": "",
            "seen_products": {},
            "price_history": {}
        }
        self.data["users"][user_id] = user_data
        self.save_data()
        return user_data
    
    def update_user(self, user_id: str, updates: Dict[str, Any]):
        if user_id in self.data["users"]:
            self.data["users"][user_id].update(updates)
            self.save_data()
    
    def get_all_active_users(self) -> Dict[str, Dict[str, Any]]:
        return {uid: data for uid, data in self.data["users"].items() 
                if data.get("active", False) and data.get("onboarding_state") == "COMPLETED"}
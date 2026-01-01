import json
import os

class URLBuilder:
    @staticmethod
    def build_url(category: str, size_label: str, price_min: int, price_max: int) -> str:
        # Load size mapping
        size_map_file = "mappings/size_map.json"
        if os.path.exists(size_map_file):
            with open(size_map_file, 'r') as f:
                size_map = json.load(f)
        else:
            size_map = {}
        
        # Get size code from mapping
        size_code = size_map.get(category, {}).get(size_label, size_label)
        
        # Build correct URL format
        url = f"https://www.timberland.co.il/{category}/footwear?price={price_min}_{price_max}&size={size_code}"
        return url

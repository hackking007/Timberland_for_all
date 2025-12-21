from config import SEARCH_URL

class URLBuilder:
    @staticmethod
    def build_url(category: str, size_code: str, price_min: int, price_max: int) -> str:
        params = []
        
        if category:
            params.append(f"gender={category}")
        
        if size_code:
            params.append(f"size={size_code}")
        
        if price_min is not None and price_max is not None:
            params.append(f"price={price_min}_{price_max}")
        
        query_string = "&".join(params)
        return f"{SEARCH_URL}?{query_string}" if query_string else SEARCH_URL
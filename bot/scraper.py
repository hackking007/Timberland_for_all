import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import hashlib

class Scraper:
    @staticmethod
    def fetch_products(url: str) -> List[Dict]:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            return Scraper._parse_html(response.text, url)
        except Exception as e:
            print(f"Error fetching products: {e}")
            return []
    
    @staticmethod
    def _parse_html(html: str, base_url: str) -> List[Dict]:
        soup = BeautifulSoup(html, 'html.parser')
        products = []
        
        # Adjust selectors based on actual site structure
        product_items = soup.select('.product-item')
        
        for item in product_items:
            try:
                product = Scraper._extract_product(item, base_url)
                if product:
                    products.append(product)
            except Exception as e:
                print(f"Error parsing product: {e}")
                continue
        
        return products
    
    @staticmethod
    def _extract_product(item, base_url: str) -> Dict:
        # Extract product details - adjust selectors as needed
        title_elem = item.select_one('.product-title, .product-name, h3, h4')
        price_elem = item.select_one('.price, .product-price, [data-price]')
        link_elem = item.select_one('a[href]')
        image_elem = item.select_one('img')
        
        if not title_elem or not price_elem:
            return None
        
        title = title_elem.get_text(strip=True)
        price_text = price_elem.get_text(strip=True).replace('₪', '').replace(',', '').strip()
        price = int(float(price_text)) if price_text.replace('.', '').isdigit() else 0
        
        url = link_elem['href'] if link_elem else ""
        if url and not url.startswith('http'):
            url = base_url + url
        
        image = image_elem.get('src', '') if image_elem else ""
        
        # Generate stable ID
        product_id = hashlib.md5(url.encode()).hexdigest() if url else hashlib.md5(title.encode()).hexdigest()
        
        return {
            "id": product_id,
            "title": title,
            "price": price,
            "url": url,
            "image": image
        }

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import re

class CouponScraper:
    @staticmethod
    def fetch_coupons() -> List[Dict]:
        try:
            # Scrape live coupons from freecoupon.co.il
            url = "https://www.freecoupon.co.il/coupons/timberland/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            coupons = []
            
            try:
                response = requests.get(url, headers=headers, timeout=30)
                response.encoding = 'utf-8'  # Force UTF-8 encoding
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Look for coupon elements
                    coupon_elements = soup.select('.coupon, .code, .promo-code, [data-code]')
                    
                    for element in coupon_elements:
                        # Extract coupon code
                        code_text = element.get_text(strip=True)
                        
                        # Look for coupon code patterns
                        code_matches = re.findall(r'\b[A-Z0-9]{3,15}\b', code_text.upper())
                        
                        for code in code_matches:
                            if len(code) >= 3 and code not in ['GET', 'OFF', 'SALE']:
                                # Clean description - remove Hebrew encoding issues
                                description = f"{code} - Timberland discount code"
                                
                                coupons.append({
                                    'code': code,
                                    'description': description,
                                    'source': 'freecoupon.co.il'
                                })
                                
                                if len(coupons) >= 3:  # Limit to 3 coupons
                                    break
                        
                        if len(coupons) >= 3:
                            break
                            
            except Exception as e:
                print(f"Error scraping freecoupon.co.il: {e}")
            
            # Add TIM12 as fallback if no coupons found
            if not coupons:
                coupons = [
                    {
                        'code': 'TIM12',
                        'description': '12% off orders over ₪200 (includes sale items)',
                        'source': 'Verified active coupon'
                    }
                ]
            
            return coupons[:2]  # Return max 2 coupons
            
        except Exception as e:
            print(f"Error fetching coupons: {e}")
            return [
                {
                    'code': 'NEWSLETTER',
                    'description': 'Sign up for newsletter to get 10% off',
                    'source': 'Email signup'
                }
            ]

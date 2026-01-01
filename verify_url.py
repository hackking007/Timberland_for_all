import sys
import os

# Add bot directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'bot')))

from url_builder import URLBuilder

def test_url_generation():
    # User Requirements:
    # Gender: Men
    # Size: 43
    # Price: 0-299
    # Expected URL: https://www.timberland.co.il/men/footwear?price=0_299&size=794
    
    category = "men"
    size_label = "43"
    price_min = 0
    price_max = 299
    
    print(f"Testing URL generation for:")
    print(f"Category: {category}")
    print(f"Size: {size_label}")
    print(f"Price: {price_min}-{price_max}")
    
    generated_url = URLBuilder.build_url(category, size_label, price_min, price_max)
    expected_url = "https://www.timberland.co.il/men/footwear?price=0_299&size=794"
    
    print(f"\nGenerated URL: {generated_url}")
    print(f"Expected URL:  {expected_url}")
    
    if generated_url == expected_url:
        print("\n✅ SUCCESS: URL matches requirements exactly.")
    else:
        print("\n❌ FAILED: URL does not match.")
        
if __name__ == "__main__":
    test_url_generation()

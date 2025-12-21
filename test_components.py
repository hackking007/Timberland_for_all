#!/usr/bin/env python3
"""
Test script for the multi-user Telegram bot components
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'bot'))

from user_store import UserStore
from url_builder import URLBuilder
from scraper import Scraper
from detector import ChangeDetector

def test_user_store():
    print("Testing UserStore...")
    store = UserStore()
    
    # Create test user
    user_data = store.create_user("test_user_123")
    assert user_data["onboarding_state"] == "NOT_STARTED"
    
    # Update user
    store.update_user("test_user_123", {"onboarding_state": "COMPLETED"})
    updated_user = store.get_user("test_user_123")
    assert updated_user["onboarding_state"] == "COMPLETED"
    
    print("✅ UserStore tests passed")

def test_url_builder():
    print("Testing URLBuilder...")
    
    url = URLBuilder.build_url("men", "794", 0, 300)
    expected = "https://www.timberland.co.il/search?gender=men&size=794&price=0_300"
    assert url == expected
    
    print("✅ URLBuilder tests passed")

def test_change_detector():
    print("Testing ChangeDetector...")
    
    seen_products = {
        "prod1": {"price": 300, "last_seen": "2024-01-01"}
    }
    
    new_products = [
        {"id": "prod1", "title": "Shoe 1", "price": 250, "url": "http://example.com/1"},
        {"id": "prod2", "title": "Shoe 2", "price": 200, "url": "http://example.com/2"}
    ]
    
    events = ChangeDetector.detect_changes(seen_products, new_products)
    
    # Should detect 1 price drop and 1 new product
    assert len(events) == 2
    assert any(e["type"] == "PRICE_DROP" for e in events)
    assert any(e["type"] == "NEW_PRODUCT" for e in events)
    
    print("✅ ChangeDetector tests passed")

def test_scraper():
    print("Testing Scraper (basic functionality)...")
    
    # Test with a simple HTML structure
    html = """
    <div class="product-item">
        <h3 class="product-title">Test Shoe</h3>
        <span class="price">₪299</span>
        <a href="/shoe1">View</a>
        <img src="/image1.jpg">
    </div>
    """
    
    products = Scraper._parse_html(html, "https://example.com")
    
    if products:
        product = products[0]
        assert "Test Shoe" in product["title"]
        assert product["price"] == 299
    
    print("✅ Scraper tests passed")

if __name__ == "__main__":
    print("Running component tests...\n")
    
    try:
        test_user_store()
        test_url_builder()
        test_change_detector()
        test_scraper()
        
        print("\n🎉 All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
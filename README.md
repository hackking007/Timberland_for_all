# Multi-User Telegram Product Tracking Bot (deployed)

A modular Telegram bot that tracks product prices and availability across multiple users with personalized filters.

## Architecture

- **Telegram Bot Interface**: Handles user interactions and commands
- **Onboarding Manager**: State machine for user setup
- **URL Generator**: Creates site-specific search URLs
- **Scraper Engine**: Fetches and parses product data
- **Change Detection**: Identifies new products and price drops
- **Notification Engine**: Sends alerts via Telegram

## Setup

1. **Create Telegram Bot**:
   - Message @BotFather on Telegram
   - Create new bot and get token
   - Add token to GitHub Secrets as `TELEGRAM_TOKEN`

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Bot Locally**:
   ```bash
   cd bot
   python telegram_bot.py
   ```

## Commands

- `/start` - Begin onboarding or show current config
- `/settings` - View current filters and URL
- `/myurl` - Get your tracking URL
- `/test` - Test scraper with your URL

## Automated Scanning

The bot runs automated scans via GitHub Actions:
- **Schedule**: Twice daily (8 AM & 8 PM UTC)
- **Manual**: Workflow dispatch available
- **State**: User data persists via git commits

## File Structure

```
bot/
├── telegram_bot.py      # Main bot interface
├── onboarding.py        # User setup flow
├── user_store.py        # Data persistence
├── url_builder.py       # URL generation
├── scraper.py           # Product fetching
├── detector.py          # Change detection
├── notifier.py          # Telegram messaging
├── scheduler_runner.py  # Automated scans
├── config.py           # Configuration
├── mappings/
│   ├── size_map.json   # Size mappings
│   └── category_map.json
└── data/
    └── user_data.json  # User state
```

## User Data Model

```json
{
  "users": {
    "user_id": {
      "onboarding_state": "COMPLETED",
      "active": true,
      "filters": {
        "category": "men",
        "size_label": "43",
        "size_code": "794",
        "price_min": 0,
        "price_max": 300
      },
      "generated_url": "https://...",
      "seen_products": {},
      "price_history": {}
    }
  }
}
```

## Extending to New Sites

1. Update `url_builder.py` with new site logic
2. Modify `scraper.py` selectors for new site structure
3. Add site-specific mappings in `mappings/`
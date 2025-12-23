import requests
import os

TOKEN = "your_bot_token_here"
VERCEL_URL = "https://your-app.vercel.app/api/webhook"

# Set webhook
response = requests.post(
    f"https://api.telegram.org/bot{TOKEN}/setWebhook",
    json={"url": VERCEL_URL}
)

print(f"Webhook set: {response.json()}")

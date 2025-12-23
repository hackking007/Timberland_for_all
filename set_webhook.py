import requests
import os


TOKEN = os.environ.get("TELEGRAM_TOKEN")  # Use environment variable
if not TOKEN:
    raise ValueError("Please set TELEGRAM_TOKEN environment variable")

# TODO: Replace with your actual Vercel production URL
# Find it at: https://vercel.com/dashboard -> Your Project -> Domains
VERCEL_URL = "https://timberland-for.vercel.app/api/webhook"  # Update this!


# Set webhook
response = requests.post(
    f"https://api.telegram.org/bot{TOKEN}/setWebhook",
    json={"url": VERCEL_URL}
)


print(f"Webhook set: {response.json()}")


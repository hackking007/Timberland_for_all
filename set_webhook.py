import requests
import os


TOKEN = os.environ.get("TELEGRAM_TOKEN")  # Use environment variable
if not TOKEN:
    raise ValueError("Please set TELEGRAM_TOKEN environment variable")

VERCEL_URL = "https://timberland-for-bm9zwsc1k-moshes-projects-2721c305.vercel.app/api/webhook"


# Set webhook
response = requests.post(
    f"https://api.telegram.org/bot{TOKEN}/setWebhook",
    json={"url": VERCEL_URL}
)


print(f"Webhook set: {response.json()}")

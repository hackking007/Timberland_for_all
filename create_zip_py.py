import zipfile
import os

def zip_project():
    files_to_zip = [
        "api/cron.py",
        "api/webhook.py",
        "bot/config.py",
        "bot/detector.py",
        "bot/mappings/size_map.json",
        "bot/mappings/category_map.json",
        "bot/notifier.py",
        "bot/onboarding.py",
        "bot/scheduler_runner.py",
        "bot/scraper.py",
        "bot/telegram_bot.py",
        "bot/url_builder.py",
        "bot/user_store.py",
        "Procfile",
        "README.md",
        "requirements.txt",
        "vercel.json"
    ]
    
    zip_name = "Timberland_Bot_Update.zip"
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_zip:
            if os.path.exists(file):
                zipf.write(file)
                print(f"Added: {file}")
            else:
                print(f"Skipping missing: {file}")
                
    print(f"Created {zip_name}")

if __name__ == "__main__":
    zip_project()

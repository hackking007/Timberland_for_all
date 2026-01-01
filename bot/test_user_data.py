import os
import json

# Check if file exists
file_path = "data/user_data.json"
print(f"Checking file: {file_path}")
print(f"File exists: {os.path.exists(file_path)}")

if os.path.exists(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    print(f"File content: {data}")
else:
    print("File not found!")
    
    # Create the file with your user data
    user_data = {
        "users": {
            "353333002": {
                "category": "men",
                "size": "43",
                "onboarding_state": "COMPLETED",
                "active": True,
                "price_min": 10,
                "price_max": 299,
                "generated_url": "https://www.timberland.co.il/men/footwear?price=10_299&size=794"
            }
        }
    }
    
    os.makedirs("data", exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(user_data, f, indent=2)
    
    print("Created user_data.json file")

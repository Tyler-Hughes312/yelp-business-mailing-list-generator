import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def fetch_yelp_categories(api_key, output_file='yelp_categories.json'):
    url = 'https://api.yelp.com/v3/categories'
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        categories = response.json().get('categories', [])
        with open(output_file, 'w') as f:
            json.dump(categories, f, indent=2)
        print(f"✅ Saved {len(categories)} categories to {output_file}")
        return categories
    else:
        print(f"❌ Error fetching categories: {response.status_code} - {response.text}")
        return []

if __name__ == "__main__":
    api_key = os.getenv('YELP_API_KEY')
    if not api_key:
        print("❌ YELP_API_KEY not found in environment.")
        exit(1)
    fetch_yelp_categories(api_key) 
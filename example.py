import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_SEARCH_API_KEY = os.environ.get('GOOGLE_SEARCH_API_KEY')
query = "Greece"
cx = "b63015b410e5247ba"

url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_SEARCH_API_KEY}&cx={cx}"

response = requests.get(url)

if response.status_code == 200:
    results = json.dumps(response.json(), indent=2)

    with open("test_resp.json", 'w') as f:
        f.write(results)
else:
    print("Error:", response.status_code, response.text)

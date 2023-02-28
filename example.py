import requests
import json
import os
from dotenv import load_dotenv
import yaml

# hidden and public config
load_dotenv()
with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# extracting config
GOOGLE_SEARCH_API_KEY = os.environ.get('GOOGLE_SEARCH_API_KEY')
CX = config['GOOGLE_SEARCH']['CX']

# query string
query = "Greece"

# send request
url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_SEARCH_API_KEY}&cx={CX}"
response = requests.get(url)

# parse request
if response.status_code == 200:
    results = json.dumps(response.json(), indent=2)

    with open("test_resp.json", 'w') as f:
        f.write(results)
else:
    print("Error:", response.status_code, response.text)

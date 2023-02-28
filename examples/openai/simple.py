import openai
import json
import os
from dotenv import load_dotenv
import yaml

# hidden and public config
load_dotenv()
with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# extract config
openai.api_key = os.environ.get('OPENAI_API_KEY')
MODEL_ENGINE = config['OPENAI']['MODEL_ENGINE']
MAX_TOKENS = config['OPENAI']['MAX_TOKENS']
TEMPERATURE = config['OPENAI']['TEMPERATURE']

# our message
message = 'Momo, jesi li ziv?'

# send request
completion = openai.Completion.create(prompt = message,
                                      engine = MODEL_ENGINE,
                                      max_tokens = MAX_TOKENS,
                                      temperature = TEMPERATURE)

results = json.dumps(completion, indent=2)
with open("examples/openai/test_resp.json", 'w') as f:
        f.write(results)
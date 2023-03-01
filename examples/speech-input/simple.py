# turn off anoying TF messages
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import whisper

model = whisper.load_model("base")
result = model.transcribe("examples/speech-input/index.wav", fp16 = False, language = 'English')

with open("examples/speech-input/test_resp.txt", 'w') as f:
        f.write(result['text'])
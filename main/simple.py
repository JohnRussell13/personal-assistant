from dotenv import load_dotenv
import yaml

# hidden and public config
load_dotenv()
with open('config.yaml') as f:
	config = yaml.load(f, Loader=yaml.FullLoader)

def record(seconds):
	import pyaudio
	import wave

	# config
	CHUNK = config['RECORD']['CHUNK']
	SAMPLE_FORMAT = pyaudio.paInt16
	CHANNELS = config['RECORD']['CHANNELS']
	FS = config['RECORD']['FS']
	FILENAME = config['RECORD']['FILENAME']

	# create audio interface and start recording
	print('Started recording')
	p = pyaudio.PyAudio()
	stream = p.open(format = SAMPLE_FORMAT,
					channels = CHANNELS,
					rate = FS,
					frames_per_buffer=CHUNK,
					input=True)

	frames = []
	for i in range(0, int(FS / CHUNK * seconds)):
		data = stream.read(CHUNK)
		frames.append(data)

	# stop recording and close audio interface
	stream.stop_stream()
	stream.close()
	p.terminate()
	print('Finished recording')

	# save as file
	wf = wave.open(FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(SAMPLE_FORMAT))
	wf.setframerate(FS)
	wf.writeframes(b''.join(frames))
	wf.close()

def transcribe():
	# HACK -- turn off anoying TF messages
	import os
	os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

	import whisper

	MODEL_TYPE = config['TRASCRIBE']['MODEL_TYPE']
	WAV_FILENAME = config['RECORD']['FILENAME']
	LANGUAGE = config['TRASCRIBE']['LANGUAGE']
	TXT_FILENAME = config['TRASCRIBE']['FILENAME']

	# transcribe 
	model = whisper.load_model(MODEL_TYPE)
	result = model.transcribe(WAV_FILENAME, fp16 = False, language = LANGUAGE)

	# os.remove(FILENAME)

	with open(TXT_FILENAME, 'w') as f:
		f.write(result['text'])

	return result['text']

def chatbot(message):
	import openai
	import os

	# extract config
	openai.api_key = os.environ.get('OPENAI_API_KEY')
	MODEL_ENGINE = config['OPENAI']['MODEL_ENGINE']
	MAX_TOKENS = config['OPENAI']['MAX_TOKENS']
	TEMPERATURE = config['OPENAI']['TEMPERATURE']
	TXT_FILENAME = config['OPENAI']['FILENAME']

	# send request
	completion = openai.Completion.create(prompt = message,
										engine = MODEL_ENGINE,
										max_tokens = MAX_TOKENS,
										temperature = TEMPERATURE)

	with open(TXT_FILENAME, 'w') as f:
		f.write(completion['choices'][0]['text'])

	return completion['choices'][0]['text']

def synth(message):
	import gtts

	# config
	WAV_FILENAME = config['SYNTH']['FILENAME']
	LANGUAGE = config['SYNTH']['LANGUAGE']

	# synthesize voice output
	tts = gtts.gTTS(message, lang = LANGUAGE)
	tts.save(WAV_FILENAME)

def play():
	import playsound
	import os

	# config
	FILENAME = config['SYNTH']['FILENAME']

	# play output
	playsound.playsound(FILENAME)

	# remove temp file
	# os.remove(FILENAME) 

record(3)
inputMessage = transcribe()
chatbotMessage = chatbot(inputMessage)
synth(chatbotMessage)
play()
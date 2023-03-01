def record():
	import pyaudio
	import wave

	chunk = 1024  # Record in chunks of 1024 samples
	sample_format = pyaudio.paInt16  # 16 bits per sample
	channels = 2
	fs = 44100  # Record at 44100 samples per second
	seconds = 3
	filename = "temp.wav"

	p = pyaudio.PyAudio()  # Create an interface to PortAudio

	print('Recording')

	stream = p.open(format=sample_format,
					channels=channels,
					rate=fs,
					frames_per_buffer=chunk,
					input=True)

	frames = []  # Initialize array to store frames

	# Store data in chunks for 3 seconds
	for i in range(0, int(fs / chunk * seconds)):
		data = stream.read(chunk)
		frames.append(data)

	# Stop and close the stream 
	stream.stop_stream()
	stream.close()
	# Terminate the PortAudio interface
	p.terminate()

	print('Finished recording')

	# Save the recorded data as a WAV file
	wf = wave.open(filename, 'wb')
	wf.setnchannels(channels)
	wf.setsampwidth(p.get_sample_size(sample_format))
	wf.setframerate(fs)
	wf.writeframes(b''.join(frames))
	wf.close()

def transcribe():
	# turn off anoying TF messages
	import os
	os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

	import whisper

	model = whisper.load_model("base")
	result = model.transcribe("temp.wav", fp16 = False, language = 'English')

	os.remove("temp.wav") 

	return result['text']

def chatbot(message):
	import openai
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

	# send request
	completion = openai.Completion.create(prompt = message,
										engine = MODEL_ENGINE,
										max_tokens = MAX_TOKENS,
										temperature = TEMPERATURE)

	return completion['choices'][0]['text']

def synth(message):
	import gtts

	tts = gtts.gTTS(message)
	tts.save("temp.wav")

def play():
	import playsound
	import os
	playsound.playsound("temp.wav")
	os.remove("temp.wav") 

record()
chatbotMessage = chatbot("Hello there")
synth(chatbotMessage)
play()
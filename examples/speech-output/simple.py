import gtts

tts = gtts.gTTS("Hello world!")
tts.save("examples/speech-output/test_resp.wav")
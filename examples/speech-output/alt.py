import gtts
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

fp = BytesIO()

message = "Hello"

tts = gtts.gTTS(text = message, lang = "en")
tts.write_to_fp(fp)
fp.seek(0)

sound = AudioSegment.from_file(fp, format="mp3")
play(sound)
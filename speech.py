from gtts import gTTS 
import os
import sound

def func(txt3):
	txt="hello "
	txt2=" . Please let me read your emotions"
	tts=gTTS(text=txt+txt3+txt2, lang='en')
	tts.save("hello.mp3")
	os.remove('welcome.wav')
	os.system("ffmpeg -i hello.mp3 welcome.wav ")
	sound.play('welcome.wav')

if __name__=='__main__':
	func()





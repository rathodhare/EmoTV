from sys import byteorder
from array import array
from struct import pack
import sys
#sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import pyaudio
import combine

THRESHOLD = 5000
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100


def welcome():
	#sound('/home/harekrissna/Desktop/ITSP/welcome.wav')
    sound('/home/harekrissna/Desktop/ITSP/sound_files/welcome.wav')
    #sound('/home/harekrissna/Desktop/ITSP/sound_files/name.wav')

def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD

def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r

def trim(snd_data):
    "Trim the blank spots at the start and end"
    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i)>THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    snd_data = _trim(snd_data)

    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data

def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    r = array('h', [0 for i in range(int(seconds*RATE))])
    r.extend(snd_data)
    r.extend([0 for i in range(int((seconds)*RATE))])
    return r

def record():
   
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)

    num_silent = 0
    snd_started = False

    r = array('h')

    while 1:

        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        silent = is_silent(snd_data)

        if silent and snd_started:
            num_silent += 1
        elif not silent and not snd_started:
            snd_started = True

        if snd_started and num_silent > 30:
            break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    r = trim(r)
    r = add_silence(r, 0.5)
    return sample_width, r

def record_to_file(path):
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack('<' + ('h'*len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()

import speech_recognition as sr

def stt(path):

    r = sr.Recognizer()
    harvard = sr.AudioFile(path)
    with harvard as source:
        audio = r.record(source)
    
    type(audio)
    txt3=r.recognize_google(audio)
    return txt3
    #speech.func(txt3)

from gtts import gTTS
import os 
import wave
def speech(txt3):
    txt='Hello '
    txt2=' . please let me read your emotions'
    tts=gTTS(text=txt+txt3+txt2, lang='en')
    tts.save("good.mp3")
    os.remove("output.wav")
    os.system("ffmpeg -i good.mp3 output.wav ")
    sound('output.wav')

import pyaudio
import wave

def speechf(txt3):
    tts=gTTS(text=txt3, lang='en')
    tts.save("good.mp3")
    os.remove("output.wav")
    os.system("ffmpeg -i good.mp3 output.wav ")
    sound('output.wav')

def songplay(emo):
	if emo==1:
		#speechf(txt)
		#speechf(', You are happy.   Let me play a song for you ')
		sound('sound_files/happyf.wav')
	if emo==2:
		#speechf(txt)
		#speechf(', You are sad .     Let me play a song for you ')
		sound('sound_files/sadf.wav')
	if emo==3:
		#speechf(txt)
		#speechf(', You are surprised .  Let me play a song for you ')
		sound('sound_files/surprisedf.wav')
    
def sound(path):
    chunk = 1024
    f = wave.open(path,"rb")
    p = pyaudio.PyAudio()
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  
    data = f.readframes(chunk)
    while data:
        stream.write(data)
        data = f.readframes(chunk)
    stream.stop_stream()
    stream.close() 
    p.terminate()

import facefinal
import ttI
def prediction():
	emo=facefinal.TakeSnapshotAndSave()
	return emo

import cv2
def show(txt):
	from PIL import Image
	img = Image.open('joined_images.jpg')
	img.show()

def ask(emo):
	#txt=txt3+',Would you like your clicked photo with personalizable options as a memory of emotv? '
	#speechf(txt)
	#wait(1)
	#record_to_file('dem.wav')
	#txt2=stt('dem.wav')
	#if txt2=='yes' or txt2=='Yes':
	show('joined_images.jpg')
	songplay(emo)
if __name__ == '__main__':
    #print("please speak a word into the microphone")
    welcome()
    #record_to_file('demo.wav')
    #txt3=stt('demo.wav')
    #txt3='L'
    #print(txt3)
    #speech(txt3)
    emo=prediction()
    print(emo)
    #ttI.ttI(txt3)
    combine.create(emo)
    ask(emo)
    #print("done - result written to demo.wav")

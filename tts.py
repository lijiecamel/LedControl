import os
from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '20157424'
API_KEY = 'AnqbtmOxiWhFEmLHQDmAjGa0'
SECRET_KEY = 'Gm1h1mV3CBFZjm6SHPqNbvVf8Ve5TQD6 '

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY) 

def tts(row,col):
	tip = "您供奉的佛像在第%s航第%s列，祝您身体健康，阖家安康"%(row+1,col+1)
	result  = client.synthesis(tip, 'zh', 1, {
		'vol': 5,
	})

	# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
	if not isinstance(result, dict):
		with open('auido.mp3', 'wb') as f:
			f.write(result)

		os.system("mplayer -af volume=30  /home/pi/ledcontrol/auido.mp3")		
''' 
import pyttsx3
engine = pyttsx3.init()
#engine.setProperty('voice','zh')
engine.setProperty('volume',15.0)
engine.say('Hello')
engine.say('您好')

engine.runAndWait()
engine.stop()
'''
import alsaaudio as alsa
import time
import audioop
import math
import RPi.GPIO as GPIO
import time


def ON(pin):
	GPIO.output(pin,GPIO.HIGH)
	return

def OFF(pin):
	GPIO.output(pin,GPIO.LOW)
	return 

def POWERGPIO(p7,p11,p13,p15,p12,p16,p18,p22):
	if(p7):
		ON(7)
	else:
		OFF(7)
	if(p11):
		ON(11)
	else:
		OFF(11)
	if(p13):
		ON(13)
	else:
		OFF(13)
	if(p15):
		ON(15)
	else:
		OFF(15)
	if(p12):
		ON(12)
	else:
		OFF(12)
	if(p16):
		ON(16)
	else:
		OFF(16)
	if(p18):
		ON(18)
	else:
		OFF(18)
	if(p22):
		ON(22)
	else:
		OFF(22)
	return

def SETGPIO(d):
	if(d == 'a'):
		POWERGPIO(0,0,0,0,0,0,0,0)
	elif(d == 'b'):
		POWERGPIO(1,0,0,0,0,0,0,0)
	elif(d == 'c'):
		POWERGPIO(1,1,0,0,0,0,0,0)
	elif(d == 'd'):
		POWERGPIO(1,1,1,0,0,0,0,0)
	elif(d == 'e'):
		POWERGPIO(1,1,1,1,0,0,0,0)
	elif(d == 'f'):
		POWERGPIO(1,1,1,1,1,0,0,0)
	elif(d == 'g'):
		POWERGPIO(1,1,1,1,1,1,0,0)
	elif(d == 'h'):
		POWERGPIO(1,1,1,1,1,1,1,0)
	elif(d == 'i'):
		POWERGPIO(1,1,1,1,1,1,1,1)
	return
print "##############################"
print "# Waiting for a song to play #"
print "##############################"

inp = alsa.PCM(alsa.PCM_CAPTURE, alsa.PCM_NORMAL, 'hw:Loopback,1,0')
out = alsa.PCM(alsa.PCM_PLAYBACK, alsa.PCM_NORMAL, 'plughw:0,0')

inp.setchannels(2)
inp.setrate(44100)
inp.setformat(alsa.PCM_FORMAT_S16_LE)
inp.setperiodsize(320)

out.setchannels(2)
out.setrate(44100)
out.setformat(alsa.PCM_FORMAT_S16_LE)
out.setperiodsize(320)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)

status = 1

lo = 10000
hi = 32000

log_lo = math.log(lo)
log_hi = math.log(hi)

while True:
	l,data = inp.read()
	if l:
		try:
			d = audioop.max(data, 2)
			vu = (math.log(float(max(audioop.max(data, 2),1)))-log_lo)/(log_hi-log_lo)
			teste = chr(ord('a')+min(max(int(vu*20),0),19))
			if teste != 'a':
				print teste
			if d>0:
				SETGPIO(teste)
				if status:
					print "Song found now playing!"
					status = 0		
		except():
			GPIO.cleanup()
			print "GPIO CLEAN"
			print "Program Closed" 
			break
		out.write(data)



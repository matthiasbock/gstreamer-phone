#!/usr/bin/python

import RPi.GPIO as GPIO
from RPi.GPIO import OUT
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

beeper = 23
GPIO.setup(beeper, OUT)

def beep(ontime=1, offtime=0):
	GPIO.output(beeper, True)
	sleep(ontime)
	GPIO.output(beeper, False)
	sleep(offtime)

def klingelton(repeats=1):
	for j in range(repeats):
		sleep(3)
		for i in range(int(1./(0.05+0.035))):
			beep(0.04, 0.035)

def keinfreizeichenton():
	for i in range(10):
		beep(0.25, 0.25)

def anrufanfangton():
	beep(0.1, 0.1)
	beep(0.1, 0.1)

def anrufendeton():
	for i in range(4):
		beep(0.5, 0.5)

def waehlton():
	beep(0.1)

if __name__ == '__main__':
	waehlton()
	sleep(1)
	keinfreizeichenton()
	sleep(1)
	waehlton()
	sleep(1)
	klingelton()
	sleep(1)
	anrufanfangton()
	sleep(1)
	anrufendeton()
	

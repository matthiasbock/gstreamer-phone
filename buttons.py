#!/usr/bin/python

import RPi.GPIO as GPIO
from RPi.GPIO import IN
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# left: pin 12, GPIO 18
# right: pin 22, GPIO 25
btnLeft = 18
btnRight = 25
GPIO.setup(btnLeft, IN)
GPIO.setup(btnRight, IN)

def pressed(button):
	return GPIO.input(button)

if __name__ == '__main__':
	import ring

	while True:
		if pressed(btnRight):
			ring.beep(0.1, 0.1)
		sleep(0.5)

#! /usr/bin/python

path = '/usr/src/gstreamer-phone'
import sys
if not path in sys.path:
	sys.path.append(path)

from subprocess import Popen, PIPE
from shlex import split
from time import sleep
from log import *

import buttons, ring
from buttons import pressed, btnLeft, btnRight
from ring import *

# testing for Raspberry Pi OpenMAX libraries
if 'uvch264' in Popen(['gst-inspect-0.10'], stdout=PIPE).communicate()[0]:
	log("gstreamer has UVC H.264 superpowers")
else:
	log("Error: gstreamer has no UVC H.264 superpowers")

# testing for webcam
if 'Logitech' in Popen(split('v4l2-ctl --list-devices'), stdout=PIPE, stderr=PIPE).communicate()[0].strip():
	log("Logitech webcam present")
else:
	log("Error: Webcam not found")

while True:
	if pressed(btnLeft):
		waehlton()
		sleep(1)
		if pressed(btnLeft): # still pressed
			if pressed(btnRight): # both pressed at once
				neustartton()
				Popen(['reboot'])
			else:
				herunterfahrton()
				Popen(['halt'])
		else:
			Popen(split('killall ssh'))
			Popen(split('killall gst-launch-0.10'))
	if pressed(btnRight):
		waehlton()
		Popen(split(path+'/streaming/paintner-to-paintner'))
		klingelton()
	sleep(0.1)

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
if 'omxh264dec' in Popen(['gst-inspect-1.0'], stdout=PIPE).communicate()[0]:
	log("gstreamer has Raspberry Pi superpowers")
else:
	log("Error: gstreamer has no Raspberry Pi superpowers")

while True:
	if pressed(btnLeft):
		waehlton()
		sleep(1)
		if pressed(btnLeft): # still pressed
			herunterfahrton()
			Popen(['halt'])
		else:
			Popen(split('killall ssh'))
			Popen(split('killall gst-launch-1.0'))
	if pressed(btnRight):
		waehlton()
		Popen(split(path+'/streaming/lohmann-to-paintner'))
		klingelton()
	sleep(0.1)

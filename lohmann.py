#! /usr/bin/python

path = '/usr/src/gstreamer-phone'
import sys
if not path in sys.path:
	sys.path.append(path)

from socket import gethostbyname
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

# parallel task
Popen(split(path+'/monitor.py'))

while True:
	#
	# Start button
	#
	if pressed(btnRight):
		log("Initiating session ...")
		waehlton()
		success = False
		try:
			ip = gethostbyname("urmel")
			log("Paintner was found in the local network at "+ip)
			success = (ip != '')
		except:
			pass
		if not success:
			try:
				ip = gethostbyname("la-cp386.no-ip.org")
				log("Paintner resolved to "+ip)
				success = True
			except:
				log("Network error: Unable to resolve Paintner's IP address. Check your LAN or WLAN connection.")
				keinfreizeichenton()
		if success:
			log("Calling "+ip+" ...")
			Popen(split(path+'/streaming/lohmann-to-paintner '+ip))
	
	#
	# Stop button
	#
	# patch: right button press also somehow invokes left button event
	if pressed(btnLeft) and not pressed(btnRight):
		waehlton()
		sleep(1)
		if pressed(btnLeft): # still pressed
			if pressed(btnRight): # both pressed at once
				log("Reboot")
				neustartton()
				Popen(['reboot'])
			else:
				log("Shutdown")
				herunterfahrton()
				Popen(['halt'])
		else:
			Popen(split('killall ssh'), stdout=PIPE, stderr=PIPE)
			Popen(split('killall gst-launch-0.10'), stdout=PIPE, stderr=PIPE)
			Popen(split('killall gst-launch-1.0'), stdout=PIPE, stderr=PIPE)
			log("Session terminated.")

	sleep(0.1)

#! /usr/bin/python

path = '/usr/src/gstreamer-phone'
import sys
if not path in sys.path:
	sys.path.append(path)

from time import sleep
from subprocess import Popen, PIPE
from shlex import split

# testing for Raspberry Pi OpenMAX libraries
if 'omxh264dec' in Popen(['gst-inspect-1.0'], stdout=PIPE).communicate()[0]:
	log("gstreamer has Raspberry Pi superpowers")
else:
	log("Error: gstreamer has no Raspberry Pi superpowers")



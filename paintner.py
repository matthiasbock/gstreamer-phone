#! /usr/bin/python

path = '/usr/src/gstreamer-phone'
import sys
if not path in sys.path:
	sys.path.append(path)

import socket
from time import sleep
from subprocess import Popen, PIPE
from shlex import split

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


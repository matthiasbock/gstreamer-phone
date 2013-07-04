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

from ring import *

def pidof(name):
	return Popen(split('pidof '+name), stdout=PIPE).communicate()[0].strip()

def ps_aux():
	return Popen(split('ps aux'), stdout=PIPE).communicate()[0].strip()

if __name__ == '__main__':
	established = False
	ringing = False

	anrufanfangton()

	while True:
		if 'ssh root@' in ps_aux():
			if pidof('gst-launch-0.10') != '' or pidof('gst-launch-1.0') != '':
				if not established:
					anrufanfangton()
					established = True
			else:
				established = False
				klingelton()
				ringing = True
		else:
			if established:
				anrufendeton()
				established = False
			elif ringing:
				keinfreizeichenton()
				ringing = False
		sleep(1)

#! /usr/bin/python

import socket
from time import sleep
from subprocess import Popen, PIPE
from shlex import split

import urllib
import re

portSIP = 5070
portRTP = 9080

def myIP():
	f = urllib.urlopen("http://www.canyouseeme.org/")
	html_doc = f.read()
	f.close()
	m = re.search('(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',html_doc)
	return m.group(0)

success = False
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while not success:
	paitnern_ip = socket.gethostbyname('la-cp386.no-ip.org')
	remote = (paintner_ip, portSIP)
	my_ip = myIP()
	msg = 'Lohmann:'+str(portRTP)
	for i in range(3):
		sock.sendto(msg, remote)
		print msg
		sleep(1)
		data, addr = self.sock.recvfrom(1024)
		if len(data) > 0:
			print 'Paintner: OK'
			success = True
			break
		else:
			print 'Paintner: no response'
del sock
	
# play video stream
Popen(split("gst-launch -v udpsrc port=9078 ! 'application/x-rtp,payload=96,encoding-name=H264' ! rtph264depay ! h264parse ! ffdec_h264 ! xvimagesink")).wait()

#! /usr/bin/python

import socket
from time import sleep
from subprocess import Popen, PIPE
from shlex import split

portSIP = 5070
portRTP = 9080

success = False
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while not success:
	paitnern_ip = resolve('la-cp386.no-ip.org')
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
		else
			print 'Paintner: no response'
del sock
	
# play video stream
Popen(split("gst-launch -v udpsrc port=9078 ! 'application/x-rtp,payload=96,encoding-name=H264' ! rtph264depay ! h264parse ! ffdec_h264 ! xvimagesink")).wait()

#! /usr/bin/python

import socket
from time import sleep
from subprocess import Popen, PIPE
from shlex import split

portSIP = 5070

# wait for Lohmann
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', portSIP))
data = ''
while len(data) == 0:
	sleep(1)
	data, addr = sock.recvfrom(1024)
	if len(data) == 0 or not 'Lohmann' in data:
		data = ''
		print 'Lohmann: did not make contact'
	else:
		print 'Lohmann: OK'
del sock

# seed video stream
Popen(split("gst-launch-0.10 uvch264_src device=/dev/video0 name=src initial-bitrate=450000 auto-start=true src.vfsrc ! queue ! 'video/x-raw-yuv,width=320,height=240' ! fakesink . src.vidsrc ! queue ! 'video/x-h264,width=1280,height=720,framerate=5/1' ! rtph264pay ! udpsink host="+addr+" port=9080").wait()

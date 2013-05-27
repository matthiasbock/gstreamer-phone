#! /usr/bin/python

from log import *
import socket
from time import sleep

class Server:
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	def listen(self, local=('', 5060)):
		# ""=any network interface
		log("Waiting for INVITE on "+local[0]+":"+str(local[1])+"(UDP) ...")
		self.local = local
		self.remote = (None, None)
		self.sock.bind( local )

	def wait(self, timeout=30):
		for i in range(int(timeout/0.1)):
			sleep(0.1)
			data, addr = self.sock.recvfrom(1024)
			if len(data) > 0:
#				log(data)
				if 'INVITE' in data:
					self.remote = addr
					log("INVITE from "+addr[0]+":"+str(addr[1])+"(UDP)")
					self.sock.sendto('OK', self.remote)
					del self.sock
					log("OK")
					return True
		return False

	def offer(self):
		Popen(split("gst-launch-1.0 v4l2src device=/dev/video0 ! 'video/x-h264' ! legacyh264parse ! rtph264pay ! udpsink host="+self.local[0]+" port=9178"), ().wait()


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
		Popen(split("cvlc v4l2:///dev/video0:chroma=h264:width=800:height=600:framerate=5/1 --sout '#rtp{sdp=rtsp://:8080/stream.sdp}' -vv").wait()


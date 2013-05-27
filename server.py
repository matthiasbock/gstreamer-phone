#! /usr/bin/python

from log import *
import socket
from time import sleep

class Server:
	def listen(self, ip='127.0.0.1', port=5060):
		# UDP
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind( (ip, port) )

	def wait(self, timeout=3000):
		for i in range(timeout/100):
			sleep(100)
			data, addr = self.sock.recvfrom(1024)
			if len(data) > 0:
				print "received message from "+addr+": "+data

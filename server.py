#! /usr/bin/python

from log import *
import socket
from time import sleep

class Server:
	def listen(self, ip='127.0.0.1', port=5060):
		# UDP
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind( (ip, port) )

	def wait(self, timeout=30):
		for i in range(int(timeout/0.1)):
			sleep(0.1)
			data, addr = self.sock.recvfrom(1024)
			if len(data) > 0:
				if 'INVITE' in data:
					log("Received INVITE from "+addr[0]+" UDP port "+str(addr[1])+".")
					return True
		return False

	def ok(self):
		self.sock.sendto('OK')

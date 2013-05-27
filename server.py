#! /usr/bin/python

from log import *
import socket
from time import sleep

class Server:
	def listen(self, local=('127.0.0.1', 5060)):
		log("Waiting for INVITE on "+local[0]+":"+str(local[1])+"(UDP) ...")
		self.local = local
		self.remote = (None, None)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
					log("OK")
					return True
		return False
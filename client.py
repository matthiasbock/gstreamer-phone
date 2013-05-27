#! /usr/bin/python

from log import *
import socket
from time import sleep

class Client:
	def __init__(self):
		self.ok = False

	def invite(self, host, port=5060):
		# UDP
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.sendto('INVITE', (host, port))
	
	def wait(self, timeout=3):
		for i in range(int(timeout/0.1)):
			sleep(0.1)
			data, addr = self.sock.recvfrom(1024)
			if len(data) > 0:
				if 'OK' in data:
					log("Received OK from "+addr[0]+" UDP port "+str(addr[1])+".")
					return True
		return False

def negotiate_streams():
	log("Negotiating session ...")
	detail("We offer no video.")
	detail("We offer no audio.")
	detail("We accept video:")
	detail2("Codec: H.264")
	detail3("800x600 @ 30 fps")
	detail("We accept no audio.")
	detail(address+" offers video:")
	detail2("Codec: H.264")
	detail3("800x600 @ 30 fps - 100 KB/s")
	detail3("1024x768 @ 30 fps - 300 KB/s")
	detail(address+" offers no audio.")
	detail(address+" accepts no video.")
	detail(address+" accepts no audio.")
	return True

def negotiate_transport():
	log("Negotiating ports ...")
	detail("Remote offers UDP port 5060. Connection test ...")
	detail2("Remote UDP port 5060 is blocked.")
	detail("Remote offers UDP port 5070. Connection test ...")
	detail2("Port ok.")
	detail("Video will arrive via RTP from remote UDP port 5070.")

def measure_bandwidth():
	log("Evaluating bandwidth:")
	detail("Transferring 10 MB of random data ...")
	detail("100 K/s.")
	detail("Receiving 10 MB of random data ...")
	detail("100 K/s.")
	return True

def select_quality_from_bandwidth():
	detail("Selecting incoming video resolution:")
	detail3("800x600 @ 30 fps, average bandwidth: 100 KB/s")
	detail("Selecting outgoing video resolution:")
	detail2("no video")
	return True

def select_lowest_quality():
	return

def establish_session():
	log("Establishing session:")
	detail(address+" will serve video stream via RTP in H264 with 800x60 @ 30 fps for lohmann.no-ip")
	detail("localhost will play RTP stream from "+address+" UDP:5070 via omxh264dec to framebuffer")
	# for subsession in gstreamer:
	#	run
	detail("Session established. Press Ctrl+C to quit ...")
	# wait until connection terminated
	# watch connection running
	# monitor bandwidth usage

def call(address):
	if '@' in address:
		log("Calling user "+user+" on "+provider+" ...")
	else:
		log("Calling host "+address+" ...")

	if connect() is None:
		log("No response. Call aborted.")
		return None
	else:
		log("Connection established.")
		if negotiate_streams():
			if measure_bandwidth():
				if select_quality_from_bandwidth():
					establish_session()
				else:
					log("Fatal: Internet connection is too slow. Call aborted.")
					return False
			else:
				log("Warning: Unable to determine internet bandwidth. Selecting lowest possible quality to ensure connection.")
				select_lowest_quality()
				establish_session()
		else:
			log("Fatal: Unable to negotiate commonly supported stream format. Call aborted.")
			return False

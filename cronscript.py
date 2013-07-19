#!/usr/bin/python

from socket import gethostbyname
from subprocess import Popen, PIPE
from shlex import split
import urllib, re
from log import log

def internetIP():
	f = urllib.urlopen("http://www.canyouseeme.org/")
	html_doc = f.read()
	f.close()
	m = re.search('(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',html_doc)
	return m.group(0)

# mDNS lookup
def lanIP():
	return gethostbyname(open('/etc/hostname').read().strip()+'.local') 

default_hosts = """127.0.0.1       localhost urmel
::1             localhost ip6-localhost ip6-loopback
fe00::0         ip6-localnet
ff00::0         ip6-mcastprefix
ff02::1         ip6-allnodes
ff02::2         ip6-allrouters
"""

def internet():
	ip = internetIP()
	log('Our external IP address is '+ip)

	f = open('/tmp/hosts','w')
	f.write(default_hosts+ip+'\tpummeluff')
	f.close()

	log("Telling la-cp386.no-ip.org ...")
	Popen(split('scp -o ConnectTimeout=5 -o StrictHostKeyChecking=no /tmp/hosts root@la-cp386.no-ip.org:/etc/')).wait()
	return ip

def lan():
	ip = lanIP()
	log('Our LAN IP address is '+ip)

	f = open('/tmp/hosts','w')
	f.write(default_hosts+ip+'\tpummeluff')
	f.close()

	log("Telling urmel.local ...")
	Popen(split('scp -o ConnectTimeout=5 -o StrictHostKeyChecking=no /tmp/hosts root@urmel.local:/etc/')).wait()
	return ip

if __name__ == '__main__':
	try:
		urmel = gethostbyname('urmel.local').strip()
		if urmel == '':
			raise
		lan()
	except:
		log("Problems contacting urmel.local.")
		internet()


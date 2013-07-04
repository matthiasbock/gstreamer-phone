#!/usr/bin/python

from subprocess import Popen
from shlex import split
import urllib, re

def myIP():
	f = urllib.urlopen("http://www.canyouseeme.org/")
	html_doc = f.read()
	f.close()
	m = re.search('(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',html_doc)
	return m.group(0)

default_hosts = """127.0.0.1       localhost urmel
::1             localhost ip6-localhost ip6-loopback
fe00::0         ip6-localnet
ff00::0         ip6-mcastprefix
ff02::1         ip6-allnodes
ff02::2         ip6-allrouters
"""

def internet():
	try:
		f = open('/tmp/hosts','w')
		f.write(default_hosts+'\n'+myIP()+'\tpummeluff')
		f.close()

		Popen(split('scp /tmp/hosts root@la-cp386.no-ip.org:/etc/'))
	except:
		pass

def lan():
	try:
		f = open('/tmp/hosts','w')
		f.write(default_hosts)
		f.close()

		Popen(split('scp /tmp/hosts root@urmel:/etc/'))
	except:
		pass

if __name__ == '__main__':
	from socket import gethostbyname
	try:
		urmel = gethostbyname('urmel').strip()
		if urmel != '':
			lan()
	except:
		internet()


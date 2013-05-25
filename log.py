#! /usr/bin/python

def now():
	return "2013-05-25 13:12"

def log(msg):
	print now()+"  "+msg

def detail(msg):
	print "\t"*3+msg

def detail2(msg):
	print "\t"*4+msg

def detail3(msg):
	print "\t"*5+msg

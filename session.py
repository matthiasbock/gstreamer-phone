#!/usr/bin/python

# play video stream
def playback()
	Popen(split("gst-launch-1.0 -v filesrc location=/dev/stdin ! h264parse ! omxh264dec ! eglglessink")).wait()

# seed video stream
def record()
	Popen(split('gst-launch-0.10 -q uvch264_src device=/dev/video1 name=src auto-start=true initial-bitrate=400000 src.vfsrc ! queue ! 'video/x-raw-yuv,width=320,height=240' ! eglglessink . src.vidsrc ! queue ! 'video/x-h264,width=1280,height=720,framerate=5/1' ! filesink location=/dev/stdout | ssh root@pikachu "gst-launch-1.0 -v filesrc location=/dev/stdin ! h264parse ! omxh264dec ! eglglessink"').wait()


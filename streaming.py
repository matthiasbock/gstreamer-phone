#!/usr/bin/python

# play video stream
def playback()
	Popen(split("gst-launch -v udpsrc port=9078 ! 'application/x-rtp,payload=96,encoding-name=H264' ! rtph264depay ! h264parse ! ffdec_h264 ! xvimagesink")).wait()

# seed video stream
def record()
	Popen(split("gst-launch-0.10 uvch264_src device=/dev/video0 name=src initial-bitrate=450000 auto-start=true src.vfsrc ! queue ! 'video/x-raw-yuv,width=320,height=240' ! fakesink . src.vidsrc ! queue ! 'video/x-h264,width=1280,height=720,framerate=5/1' ! rtph264pay ! udpsink host="+addr+" port=9080").wait()

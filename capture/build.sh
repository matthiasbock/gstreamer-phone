#!/bin/sh

gcc -O2 -w `pkg-config --cflags --libs libv4l2` capture.c -o capture
gcc -O2 -w `pkg-config --cflags --libs libv4l2` config.c -o config

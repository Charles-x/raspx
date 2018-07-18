#!/usr/bin/env python
#coding:utf-8

from picamera import PiCamera
import time
"""set camera"""
camera = PiCamera()
camera.resolution = (320,240)
camera.framerate = 15

camera.start_preview()
time.sleep(1)
camera.capture('/home/pi/Pictures/test.jpg')
camera.stop_preview()


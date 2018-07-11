#!/usr/bin/env python
#coding:utf-8

from picamera import PiCamera
import time
"""set camera"""
camera = PiCamera()
camera.resolution = (800,600)
camera.framerate = 30

camera.start_preview()
time.sleep(1)
camera.capture('/home/pi/testme.jpg')
camera.stop_preview()


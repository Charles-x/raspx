#!/usr/bin/env python
#coding:utf-8

from picamera import PiCamera
import time
import datetime
"""set camera"""
camera = PiCamera()
camera.resolution = (800,600)
camera.framerate = 15

camera.start_preview()
time.sleep(2)
camera.capture('/home/pi/Pictures/test.jpg')
nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
camera.stop_preview()

from PIL import Image
from PIL import ImageDraw
imageFile = "/home/pi/Pictures/test.jpg"
im1=Image.open(imageFile)
draw = ImageDraw.Draw(im1)
draw.text((0, 0),nowTime,(255,255,0))
draw = ImageDraw.Draw(im1)
im1.save("/home/pi/Pictures/test.jpg")


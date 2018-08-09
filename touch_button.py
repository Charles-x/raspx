#!/usr/bin/env python
#coding:utf-8


import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
touch_pin = 22
water_relay_pin = 5
GPIO.setup(touch_pin,GPIO.OUT)
GPIO.output(touch_pin,GPIO.LOW)
GPIO.setup(touch_pin,GPIO.IN,GPIO.PUD_UP)

import relay

rp = relay.Relay(water_relay_pin)

while 1:
    try:
        if GPIO.wait_for_edge(touch_pin, GPIO.RISING):
            rp.twinkle(0.2,0.5,5)
    except KeyboardInterrupt:
        break
#!/usr/bin/env python
#coding:utf-8

import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
water_relay_pin = 5

GPIO.setup(water_relay_pin,GPIO.OUT)
for i in range(5):
    GPIO.output(water_relay_pin,GPIO.LOW)

    sleep(1)
    print "-"
    GPIO.output(water_relay_pin,GPIO.HIGH)
    sleep(1)
cleanup = GPIO.cleanup()
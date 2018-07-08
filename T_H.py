#!/usr/bin/env python
#coding:utf-8

import RPi.GPIO as GPIO
import time

TH_pin = 6

data = []
j = 0

GPIO.setmode(GPIO.BCM)
time.sleep(1)
GPIO.setup(TH_pin, GPIO.OUT)
GPIO.output(TH_pin, GPIO.LOW)
time.sleep(0.02)
GPIO.output(TH_pin, GPIO.HIGH)
GPIO.setup(TH_pin, GPIO.IN)

while GPIO.input(TH_pin) == GPIO.LOW:
    continue

while GPIO.input(TH_pin) == GPIO.HIGH:
    continue

while j < 40:
    k = 0
    while GPIO.input(TH_pin) == GPIO.LOW:
        continue
    while GPIO.input(TH_pin) == GPIO.HIGH:
        k += 1
        if k > 100:
            break
    if k < 8:
        data.append(0)
    else:
        data.append(1)
    j += 1

print "sensor is working."
GPIO.cleanup()

print data

humidity_bit = data[0:8]
humidity_point_bit = data[8:16]
temperature_bit = data[16:24]
temperature_point_bit = data[24:32]
check_bit = data[32:40]

humidity = 0
humidity_point = 0
temperature = 0
temperature_point = 0
check = 0

for i in range(8):
    humidity += humidity_bit[i] * 2 ** (7 - i)
    humidity_point += humidity_point_bit[i] * 2 ** (7 - i)
    temperature += temperature_bit[i] * 2 ** (7 - i)
    temperature_point += temperature_point_bit[i] * 2 ** (7 - i)
    check += check_bit[i] * 2 ** (7 - i)

tmp = humidity + humidity_point + temperature + temperature_point

if check == tmp:
    print "temperature : ", temperature, ", humidity : ", humidity
else:
    print "########wrong########"
    print "temperature : ", temperature, ", humidity : ", humidity, " check : ", check, " tmp : ", tmp
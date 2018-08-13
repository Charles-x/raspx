#!/usr/bin/env python
#coding:utf-8

import RPi.GPIO as GPIO
from time import sleep


class Relay:
    __pin = 0

    def __init__(self, pin):
        self.__state = False
        self.__pin = pin
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__pin,GPIO.OUT)
        GPIO.output(self.__pin,GPIO.HIGH)

    def connect(self,second):
        GPIO.output(self.__pin,GPIO.LOW)
        self.__state = True
        sleep(second)
        self.__end__()

    def twinkle(self,working_time=1,interval_time=1,times=3):
        time = 0
        while time < times:
            self.connect(working_time)
            sleep(interval_time)
            time += 1

    @property
    def status(self):
        return self.__state

    def __end__(self):
        GPIO.output(self.__pin,GPIO.HIGH)
        self.__state = False

    def __del__(self):
        GPIO.cleanup(self.__pin)


if __name__ == '__main__':
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    water_relay_pin = 26
    rp = Relay(water_relay_pin)
    print rp.status
    rp.twinkle(1,1,3)
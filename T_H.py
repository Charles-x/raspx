#!/usr/bin/env python
#coding:utf-8

import RPi.GPIO as GPIO
import time
import json


class T_H(object):
    def __init__(self,THpin):
        self.TH_pin = THpin
        # self.data = None
        GPIO.setmode(GPIO.BCM)
        time.sleep(0.8)
        GPIO.setup(self.TH_pin, GPIO.OUT)
        GPIO.output(self.TH_pin, GPIO.LOW)

    def get_data(self):
        data = []
        times = 0
        time.sleep(0.02)
        GPIO.output(self.TH_pin, GPIO.HIGH)
        GPIO.setup(self.TH_pin, GPIO.IN)
        while GPIO.input(self.TH_pin) == GPIO.LOW:
            continue
        while GPIO.input(self.TH_pin) == GPIO.HIGH:
            continue
        while times < 40:
            Voh = 0
            while GPIO.input(self.TH_pin) == GPIO.LOW:
                continue
            while GPIO.input(self.TH_pin) == GPIO.HIGH:
                Voh += 1
                if Voh > 100:
                    break
            if Voh < 8:
                data.append(0)
            else:
                data.append(1)
            times += 1
        # print "sensor is working."
        return data

    @staticmethod
    def parse_data(data):
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
        data_tmp = humidity + humidity_point + temperature + temperature_point
        # print "data_tmp",tmp
        # print "check",check
        # print humidity,humidity_point,temperature,temperature_point
        if check == data_tmp:
            check = True
            return json.dumps({"check":check,"data":[{"humidity":humidity+float(humidity_point)/10,
                                                      "temperature":temperature+float(temperature_point)/10}]})
        else:
            return json.dumps({"check": False, "data": [{"check": check,
                                                         "data_tmp": data_tmp}]})

    def data_check(self):
        #TODO:data validity check use binary data.
        pass


    def auto_getdata(self):
        data = self.get_data()
        #TODO:If data is invalid,get data repeat until is valid.


    def __delete__(self):
        GPIO.cleanup()

if __name__ == '__main__':
    T = T_H(THpin=6)
    # print T.get_data()
    # data = [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0]
    print T_H.parse_data(T.get_data())


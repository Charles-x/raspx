#!/usr/bin/env python
#coding:utf-8

import RPi.GPIO as GPIO
import time


class T_H(object):
    def __init__(self,THpin):
        self.TH_pin = THpin
        self.check = None
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        time.sleep(1)
        GPIO.setup(self.TH_pin, GPIO.OUT)
        GPIO.output(self.TH_pin, GPIO.LOW)

    def get_data(self,parse_check):
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
        if parse_check:
            return self.data_check(self.parse_data(data))
        else:
            return data

    def parse_data(self,data):
        if not data:
            return False
        data_item = ("humidity_bit", "humidity_point_bit", "temperature_bit", "temperature_point_bit", "check_bit")
        data_tmp = {"check": None, "data": {}}
        for i, d in zip(range(0, 41, 8), range(5)):
            data_tmp["data"].update(dict([(data_item[d], int(reduce(lambda a, b: str(a) + str(b), data[i:i + 8]), 2))]))

        return data_tmp

    def data_check(self,data_tmp):
        if not data_tmp:
            self.check = None
            return False

        if sum(data_tmp["data"].values()) - data_tmp["data"]["check_bit"]*2 == 0:
            data_tmp["check"] = True
            self.check = True
            return data_tmp
        else:
            data_tmp["check"] =False
            self.check = False
            return data_tmp

    def datea(self,data):
        #{'data': {'temperature_bit': 14, 'humidity_point_bit': 128, 'temperature_point_bit': 128, 'check_bit': 50, 'humidity_bit': 163}, 'check': False}
        T_H = data['data']
        datea = {'data': {'temperature': T_H["temperature_bit"]+T_H["temperature_point_bit"]/10.0,
                          'humidity': T_H["humidity_bit"]+T_H["humidity_point_bit"]/10.0,
                          'check_bit': T_H["check_bit"]},
                 'check': data["check"],"date":time.time()}
        return datea

    def auto_getdata(self,errortimes=3):
        for i in range(errortimes+1):
            data = self.get_data(True)
            if self.check == True:
                return self.datea(data)
            else:
                self.reset()
        return {"date":time.time(), 'data': 'Error', 'check': False}

    def reset(self):
        print "reset"
        self.__delete__()
        time.sleep(1)
        self.__init__(self.TH_pin)

    def __delete__(self):
        GPIO.cleanup()

if __name__ == '__main__':
    T = T_H(THpin=6)
    # print T.get_data()
    # data = [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0]

    print T.auto_getdata()


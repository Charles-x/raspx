#!/usr/bin/env python
#coding:utf-8
import PCF8591 as ADC
import time




def setup():
    ADC.setup(0x48)


def loop():
    maxvalue = 0
    minvalue = 255
    maxvalue2 = 0
    minvalue2 = 255
    num = 1
    while True:
        value = ADC.read(0)
        value2 = ADC.read(1)
        minvalue = min(minvalue,value)
        maxvalue = max(maxvalue,value)
        minvalue2 = min(minvalue2,value2)
        maxvalue2 = max(maxvalue2,value2)
        print "="*10,str(num),"="*10
        print 'light intensity: {}    min: {},max: {}'.format(value,minvalue,maxvalue)
        print 'Soil humidity : {}   min: {},max: {}'.format(value2,minvalue2,maxvalue2)
        print
        num += 1
        time.sleep(1)


if __name__ == '__main__':
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        pass
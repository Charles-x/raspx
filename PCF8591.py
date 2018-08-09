#!/usr/bin/env python
#coding:utf-8
import smbus
import time

class xADC:
    '''
    #------------------------------------------------------
    #
    #    This is a program for PCF8591 Module.
    #
    #    Warnng! The Analog input MUST NOT be over 3.3V!
    #
    #    In this script, we use a poteniometer for analog
    #   input, and a LED on AO for analog output.
    #
    #    you can import this script to another by:
    #	import PCF8591 as ADC
    #
    #	ADC.Setup(Address)  # Check it by sudo i2cdetect -y 1
    #	ADC.read(channal)	# Channal range from 0 to 3
    #	ADC.write(Value)	# Value range from 0 to 255
    #
    #------------------------------------------------------
    '''
    def __init__(self,Addr=0x48):
        # for RPI version 1, use "bus = smbus.SMBus(0)
        if not Addr:
            return {'status':'error','message':'Check it by sudo i2cdetect -y 1'}
        self.address = Addr
        self.bus = smbus.SMBus(1)

    def read(self,chn): #channel
        try:
            if chn == 0:
                self.bus.write_byte(self.address,0x40)
            if chn == 1:
                self.bus.write_byte(self.address,0x41)
            if chn == 2:
                self.bus.write_byte(self.address,0x42)
            if chn == 3:
                self.bus.write_byte(self.address,0x43)
                self.bus.read_byte(self.address) # dummy read to start conversion
        except Exception, e:
            print "Address: %s" % self.address
            print e
        return self.bus.read_byte(self.address)

    def write(self,val):
        try:
            temp = val # move string value to temp
            temp = int(temp) # change string to integer
            # print temp to see on terminal else comment out
            bus.write_byte_data(address, 0x40, temp)
        except Exception, e:
            print "Error: Device address: 0x%2X" % address
            print e

    def auto_read(self):
        data = {'status':'ok','data':{"light":self.read(0),"T":self.read(1),"external":self.read(2),"0-5v":self.read(3)}}
        return data

if __name__ == "__main__":
    adc = xADC()
    while True:
        print 'AIN0 = ', adc.read(0), "light"
        print 'AIN1 = ', adc.read(1), "T"
        print 'AIN2 = ', adc.read(2), "external"
        print 'AIN3 = ', adc.read(3), "0-5v"
        tmp = read(0)
        tmp = tmp*(255-125)/255+125 # LED won't light up below 125, so convert '0-255' to '125-255'
        write(tmp)
        time.sleep(1)
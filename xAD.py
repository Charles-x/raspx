#!/usr/bin/env python
# coding:utf-8

from __future__ import division
import smbus
import time



# 0x00 - 0x03 is AIN0 - AIN3
# bus.write_byte(address,0x00)
class xADC:
    '''
    #------------------------------------------------------
    #    0x00 - 0x03 is AIN0 - AIN3
    #    bus.write_byte(address,0x00)
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
        '''for RPI version 1, use "bus = smbus.SMBus(0)'''
        if not Addr:
            raise {'status':'error','message':'Check it by sudo i2cdetect -y 1'}
        self.address = Addr
        self.bus = smbus.SMBus(1)

    def read(self,AIN): #channel
        if AIN ==0:
            adr = 0x40
        elif AIN ==1:
            adr = 0x41
        elif AIN ==2:
            adr = 0x42
        elif AIN ==3:
            adr = 0x43
        try:
            self.bus.write_byte(self.address, adr)
            self.bus.read_byte(self.address)  # dummy read to start conversion
            temp = self.bus.read_byte(self.address)
            return temp
        except Exception as e:
            return e
        finally:
            pass

    def write(self,var_int):
        '''
        write to ANIOUT
        '''
        try:
            self.bus.write_byte_data(self.address, 0x40, var_int)
            return self.read(2)
        except Exception as e:
            return (e,"Error: Device address: 0x%2X" % self.address)


    def auto_read(self):
        '''
        'AIN0 = P5 = light      = 0x41 '
        'AIN1 = P4 = T          = 0x42 '
        'AIN2 = P5 = 0~5V       = 0x43 '
        'AIN3 = P6 = soil       = 0x40 '
        'AOUT -> AIN2
        :return:
        '''
        data = {'status':'ok','data':{"light":self.read(0),"T":self.read(1),"external":self.read(3),"0-5v":self.read(2)}}
        return data

    def interpret(self):
        '''
        #light
        :230 > light > 250,Dark
        :200 > light > 230,Light
        :180 > light > 200,Bright
        :100 > light > 180,Very bright
        :000 > light > 100,Bright blind
        #soil
        :100 < soil < 255
        :threshold = 135
        '''
        light = self.read(0)
        soil = self.read(3)
        light_s = ""
        soil_s = ""
        if 230 <= light <= 255:
            light_s = "好黑"
        elif 200 <= light < 230:
            light_s = "有点光"
        elif 180 <= light < 200:
            light_s = "亮"
        elif 100 <= light < 180:
            light_s = "很亮"
        elif 0 <= light < 100:
            light_s = "亮瞎"
        soil_p = round((1- (soil-80)/175),1)*10
        if soil < 100:
            soil_s = "水有点多"
        elif soil < 135:
            soil_s = "该浇水了"
        elif soil < 200:
            soil_s = "好干"
        elif soil <= 255:
            soil_s = "特干"
        data = {'status':'ok','data':{"light":light,"light_s":light_s,"T":self.read(1),"soil":soil,"soil_s":soil_s,"soil_p":soil_p,"0-5v":self.read(2)}}
        return data



if __name__ == "__main__":
    adc = xADC()
    while True:
        print 'AIN0 = P5 = light = 0x41 ', adc.read(0)
        print 'AIN1 = P4 = T     = 0x42 ', adc.read(1)
        print 'AIN2 = P5 = None  = 0x43 ', adc.read(2)
        print 'AIN3 = P6 = 0~5V  = 0x40 ', adc.read(3)
        print '\n'*5
        # tmp = adc.read(0)
        # tmp = tmp*(255-125)/255+125 # LED won't light up below 125, so convert '0-255' to '125-255'
        # adc.write(200)
        time.sleep(1)
        #"external"
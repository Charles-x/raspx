#!/usr/bin/env python
# -*- coding=utf8 -*-


import socket
import struct
import RPi.GPIO as GPIO
import datetime


class touch2wol(object):
    def __init__(self, mac, broadcast_ip):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.touch_pin = 22
        GPIO.setup(self.touch_pin, GPIO.OUT)
        GPIO.output(self.touch_pin, GPIO.LOW)
        GPIO.setup(self.touch_pin, GPIO.IN, GPIO.PUD_UP)
        self.mac_address = mac
        self.broadcast_ip = broadcast_ip

    def WOL(self):
        mac_adress = ""
        if len(self.mac_address) == 12:
            pass
        elif len(self.mac_address) == 12 + 5:
            sep = self.mac_address[2]
            mac_adress = self.mac_address.replace(sep, '')
        else:
            raise ValueError('Incorrect MAC address format')
        data = ''.join(['FFFFFFFFFFFF', mac_adress * 16])
        send_data = b''
        for i in range(0, len(data), 2):
            byte_dat = struct.pack('B', int(data[i: i + 2], 16))
            send_data = send_data + byte_dat
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(send_data, (self.broadcast_ip, 7))
        sock.close()
        info = "{}  WOL data packet have been sent to {}!".format(
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            mac_address)
        return info

    def start(self):
        while 1:
            print("Wait for touch to the Button!")
            try:
                if GPIO.wait_for_edge(self.touch_pin, GPIO.RISING):
                    print(self.WOL())
            except Exception as e:
                print(e)
                break


if __name__ == '__main__':
    mac_address = '00:90:f5:eb:3b:d4'
    broadcast = '192.168.199.255'
    tw = touch2wol(mac_address, broadcast)
    tw.start()

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 14:07:18 2018

@author: kudod
"""

import serial
ser = serial.Serial('COM7',9600,timeout=10)
ser.flushInput()
while True:
    try:
        ser_bytes = ser.readline()
        decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8")
        print(decoded_bytes)
        
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        break
ser.close()

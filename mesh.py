#!/usr/bin/python
from sys import stdout

import serial
from struct import pack


ser = serial.Serial(
    #port='/dev/ttyACM0',\
    port='/dev/tty.usbmodem1411',\
    baudrate=115200,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)


def proportion(value, istart, istop, ostart, ostop):
    return float(ostart) + (float(ostop) - float(ostart)) * ((float(value) - float(istart)) / (float(istop) - float(istart)))


while True:

    data = ser.read(28)

    if ((len(data) == 28) and (ord(data[0]) == 254) and (ord(data[1]) == 255)): # protect from bad readings
        panelTouched = (ord(data[18]) << 24) + (ord(data[18]) << 16) + (ord(data[17]) << 8) + ord(data[16])
        if (panelTouched >0 ):
            panelTouched = True
        else :
            panelTouched = False

        x = (ord(data[23]) << 8) + ord(data[22])
        y = (ord(data[25]) << 8) + ord(data[24])
        z = (ord(data[27]) << 8) + ord(data[26])

        print str(x) + " " + str(y) + " " + str(z)
        stdout.flush()

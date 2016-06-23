#!/usr/bin/python
from sys import stdout

import serial
from struct import pack

filterStrength = 10

ser = serial.Serial(
    #port='/dev/ttyACM0',\
    port='/dev/tty.usbmodem1411',\
    baudrate=115200,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=None)

def calculateMean(mean, listN, n):
    del listN[0]
    listN.append(mean)
    mean = 0
    for a in listN:
        mean+=a
    mean+=n
    mean/=len(listN)+1
    return mean


listX = []
listY = []
listZ = []

for a in range(filterStrength):
    listX.append(0)
    listY.append(0)
    listZ.append(0)

meanX = 0
meanY = 0
meanZ = 0

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

        meanX = calculateMean(meanX, listX, x)
        meanY = calculateMean(meanY, listY, y)
        meanZ = calculateMean(meanZ, listZ, z)
        

        print str(meanX) + " " + str(meanY) + " " + str(meanZ)
        stdout.flush()

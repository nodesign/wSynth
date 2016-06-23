import serial
from struct import pack
from time import sleep

ser = serial.Serial(
    #port='/dev/ttyACM0',\
    port='/dev/tty.usbmodem1411',\
    baudrate=115200,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=None)

def proportion(value, istart, istop, ostart, ostop):
    return float(ostart) + (float(ostop) - float(ostart)) * ((float(value) - float(istart)) / (float(istop) - float(istart)))

print("connected to: " + ser.portstr)
midi = None
try :
    midi = open("/dev/midi1", "w")
except :
    midi = None
    print "Midi 1 don't exist\nWill simulate"

def send(data):
    global midi
    if not(midi is None):
        midi.write(data)
        midi.flush()

lastVal = 0
note = 0
noteList = []
blocked  = False
cnt = 0
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

        #print str(x) + " " + str(y) + " " + str(z) + " " + str(panelTouched)
        if (x > 39000) :
            x = 39000
        if (x < 21000) :
            x = 21000

        if (y < 29000) :
            y = 29000
        if (y > 50000) :
            y = 50000
            
        if (z > 46000) :
            z = 46000

        noteX = int(proportion(x, 39000,21000, 0,11))
        octaveY = int(proportion(y, 29000,50000, 0,10))

        note = noteX*12+octaveY

        z = int(proportion(z,0,46000, 0,16383))



        if (z != lastVal):
            delta = abs(z-lastVal)
            if (cnt < 5):
                cnt+=1
            else :
                if (delta!=16383):
                    print "CC on 224 ",z, " 0"
                    a = z >> 7
                    b = z & 0x7F
                    send(pack("BBBB", 224,a,b,0))
                    #send(pack("BBB", 176,11,z)) # control change, vibratio rate            
                    lastNote = z
                cnt = 0
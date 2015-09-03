#!/usr/bin/python

## @package rpisigfox
#  This script allow the control of the rpisigfox expansion board for Raspberry Pi.
#
#  V1.0 allow only to send regular message on the SigFox Network.
#  syntax is :
#  sendsigfox MESSAGE 
#  where MESSAGE is a HEXA string encoded. Can be 2 to 24 characters representing 1 to 12 bytes.
#  Example : sendsigfox 00AA55BF to send the 4 bytes 0x00 0xAA 0x55 0xBF
# 

import time
import serial
import sys
from time import sleep

SOH = chr(0x01)
STX = chr(0x02)
EOT = chr(0x04)
ACK = chr(0x06)
NAK = chr(0x15)
CAN = chr(0x18)
CRC = chr(0x43)

def getc(size, timeout=1):
    return ser.read(size)

def putc(data, timeout=1):
    ser.write(data)
    sleep(0.001) # give device time to prepare new buffer and start sending it

def WaitFor(ser, s, timeOut):
        nbMax = 0
        ser.timeout = timeOut
        currentMsg = ''
        while currentMsg.endswith(s) != True :
            # should add a try catch here
            c=ser.read()
            if c != '' :
                currentMsg += c
            else :
                print 'timeout waiting for ' + s
                return False
            nbMax = nbMax + 1
            if nbMax > 150:
		print 'Timeout expired'
		return False
        return True

print('Sending SigFox Message...\n')

ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
)
ser.open()

ser.write('AT\r')

if (WaitFor(ser, 'OK', 3)):
  print('SigFox Modem OK')
else:
  print('SigFox Modem Error')
  ser.close()
  exit()

ser.write("AT$SS={0}\r".format(sys.argv[1]))
print('Sending ...')
if (WaitFor(ser, 'OK', 15)):
  print('OK Message sent')
else:
  print('Error Sending message')
  ser.close()
  exit()

ser.close()

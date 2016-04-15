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

def WaitFor(success, failure, timeOut):
    return ReceiveUntil(success, failure, timeOut) != ''

def ReceiveUntil(success, failure, timeOut):
	iterCount = timeOut / 0.1
	ser.timeout = 0.1
	currentMsg = ''
	while iterCount >= 0 and success not in currentMsg and failure not in currentMsg :
		sleep(0.1)
		while ser.inWaiting() > 0 : # bunch of data ready for reading
			c = ser.read()
			currentMsg += c
		iterCount -= 1
	if success in currentMsg :
		return currentMsg
	elif failure in currentMsg :
		print 'Failure (' + currentMsg.replace('\r\n', '') + ')'
	else :
		print 'Receive timeout (' + currentMsg.replace('\r\n', '') + ')'
	return ''

print 'Sending SigFox Message...'

# allow serial port choice from parameter - default is /dev/ttyAMA0
portName = '/dev/ttyAMA0'
if len(sys.argv) == 3:
    portName = sys.argv[2]

print 'Serial port : ' + portName

ser = serial.Serial(
	port=portName,
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)

if(ser.isOpen() == True): # on some platforms the serial port needs to be closed first 
    ser.close()

try:
    ser.open()
except serial.SerialException as e:
    sys.stderr.write("Could not open serial port {}: {}\n".format(ser.name, e))
    sys.exit(1)

ser.write('AT\r')
if WaitFor('OK', 'ERROR', 3) :
	print('SigFox Modem OK')

	ser.write("AT$SS={0}\r".format(sys.argv[1]))
	print('Sending ...')
	if WaitFor('OK', 'ERROR', 15) :
		print('OK Message sent')

else:
	print 'SigFox Modem Error'

ser.close()

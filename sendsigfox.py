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

class Sigfox(object):
    SOH = chr(0x01)
    STX = chr(0x02)
    EOT = chr(0x04)
    ACK = chr(0x06)
    NAK = chr(0x15)
    CAN = chr(0x18)
    CRC = chr(0x43)

    def __init__(self, port):
        # allow serial port choice from parameter - default is /dev/ttyAMA0
        portName = port
        
        print 'Serial port : ' + portName
        self.ser = serial.Serial(
                port=portName,
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
        )

    def getc(self, size, timeout=1):
        return ser.read(size)

    def putc(self, data, timeout=1):
        ser.write(data)
        sleep(0.001) # give device time to prepare new buffer and start sending it

    def WaitFor(self, success, failure, timeOut):
        return self.ReceiveUntil(success, failure, timeOut) != ''

    def ReceiveUntil(self, success, failure, timeOut):
            iterCount = timeOut / 0.1
            self.ser.timeout = 0.1
            currentMsg = ''
            while iterCount >= 0 and success not in currentMsg and failure not in currentMsg :
                    sleep(0.1)
                    while self.ser.inWaiting() > 0 : # bunch of data ready for reading
                            c = self.ser.read()
                            currentMsg += c
                    iterCount -= 1
            if success in currentMsg :
                    return currentMsg
            elif failure in currentMsg :
                    print 'Failure (' + currentMsg.replace('\r\n', '') + ')'
            else :
                    print 'Receive timeout (' + currentMsg.replace('\r\n', '') + ')'
            return ''

    def sendMessage(self, message):
        print 'Sending SigFox Message...'
        
        if(self.ser.isOpen() == True): # on some platforms the serial port needs to be closed first 
            self.ser.close()

        try:
            self.ser.open()
        except serial.SerialException as e:
            sys.stderr.write("Could not open serial port {}: {}\n".format(ser.name, e))
            sys.exit(1)

        self.ser.write('AT\r')
        if self.WaitFor('OK', 'ERROR', 3) :
                print('SigFox Modem OK')

                self.ser.write("AT$SS={0}\r".format(message))
                print('Sending ...')
                if self.WaitFor('OK', 'ERROR', 15) :
                        print('OK Message sent')

        else:
                print 'SigFox Modem Error'

        self.ser.close()

if __name__ == '__main__':
    
    if len(sys.argv) == 3:
            portName = sys.argv[2]
            sgfx = Sigfox(portName)
    else:
        sgfx = Sigfox('/dev/ttyAMA0')
        
    message = "1234CAFE"
    if len(sys.argv) > 1:
        message = "{0}".format(sys.argv[1])
    sgfx.sendMessage(message)
    #time.sleep(600) #sleep for 10 min

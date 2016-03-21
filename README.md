# rpisigfox board control script

##### Aim of this script is to control the rpisigfox board to send messages on the SigFox network.
The expansion board is for raspberry pi mainboard and allow to use the [SigFox network](http://sigfox.com)

You can purchase the board on [YADOM.FR](http://yadom.fr/carte-rpisigfox.html).

The script is a simple python script used to send data.

##### Usage

The script can be used simply by calling:
'sendsigfox MESSAGE [path/to/serial]'

Second parameter is optional.
 
where MESSAGE is a HEXA string encoded. Can be 2 to 24 characters representing 1 to 12 bytes.

Examples :
- 'sendsigfox 00AA55BF' to send the 4 bytes 0x00 0xAA 0x55 0xBF
- 'sendsigfox CCDD /dev/ttyS0' to send the 2 bytes 0xCC 0xDD over port /dev/ttyS0

##### Prerequist

Disable Raspberry Pi terminal on serial port with raspi-config utility:
sudo raspi-config
9 Advanced Options >> A8 Serial >> NO

Install pyserial
sudo apt-get install python-serial

##### License

MIT License / read license.txt

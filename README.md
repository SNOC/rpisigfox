# rpisigfox board control script

##### Aim of this script is to control the rpisigfox board to send messages on the SigFox network.
The expansion board is for raspberry pi mainboard and allows to use the [SigFox network](http://sigfox.com)

You can purchase the board on [YADOM.FR](http://yadom.fr/carte-rpisigfox.html).

Two python scripts are provided :

- sendsigfox.py sends data over the Sigfox network.

- sendreceivesigfox.py sends data with a downlink message request. Downlink messages are 8 bytes long. BEWARE : Sigfox operators may bill downlink messages, please refer to your contract.

##### Usage

'sendsigfox MESSAGE [path/to/serial]'
'sendreceivesigfox MESSAGE [path/to/serial]'
 
- MESSAGE is an HEXA encoded string; 2 to 24 characters representing 1 to 12 bytes.

- Second parameter an the optional path to the serial port, default is /dev/ttyAMA0.

Examples :
- 'sendsigfox 00AA55BF' : sends the 4 bytes 0x00 0xAA 0x55 0xBF
- 'sendsigfox CCDD /dev/ttyS0' : sends the 2 bytes 0xCC 0xDD over /dev/ttyS0
- 'sendreceivesigfox 0123456789' : sends the 5 bytes 0x01 0x23 0x45 0x67 0x89 with a downlink request

##### Prerequist

Disable Raspberry Pi terminal on serial port with raspi-config utility:

sudo raspi-config

9 Advanced Options >> A8 Serial >> NO

Install pyserial

sudo apt-get install python-serial

##### Pi3 requirements

In '/boot/config.txt' disable if present 'dtoverlay=pi3-miniuart-bt' by adding a '\#' character at line begining

Add if necessary :

dtoverlay=pi3-disable-bt

enable_uart=1

Then reboot : 

sudo reboot

Serial port to use is the script's default one : /dev/ttyAMA0

##### License

MIT License / read license.txt
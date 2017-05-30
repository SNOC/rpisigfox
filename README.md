# rpisigfox board control script

##### Aim of this script is to control the rpisigfox board to send messages on the SigFox network.
The expansion board is for raspberry pi mainboard and allows sending messages over the [SigFox network](http://sigfox.com)

You can purchase the board on [YADOM.FR](http://yadom.fr/carte-rpisigfox.html).

Two python scripts are provided :
- sendsigfox.py sends data over the Sigfox network.
- sendreceivesigfox.py sends data with a downlink message request. Downlink messages are 8 bytes long. **_Important note_** : Sigfox operators may bill downlink messages, please refer to your contract.

# Usage
```bash
./sendsigfox.py MESSAGE [path/to/serial]
./sendreceivesigfox.py MESSAGE [path/to/serial]
```
#### Where:
- ```MESSAGE``` is an hexadecimal encoded string; 2 to 24 characters representing 1 to 12 bytes.
- ```path/to/serial``` is an optional path to the serial port, default is ```/dev/ttyAMA0```.

#### Examples :
- ```./sendsigfox.py 00AA55BF``` : sends the 4 bytes 0x00 0xAA 0x55 0xBF over default serial port ```/dev/ttyAMA0```
- ```./sendsigfox.py CCDD /dev/ttyS0``` : sends the 2 bytes 0xCC 0xDD over serial port ```/dev/ttyS0```
- ```./sendreceivesigfox.py 0123456789``` : sends the 5 bytes 0x01 0x23 0x45 0x67 0x89 with a downlink request over default serial port ```/dev/ttyAMA0```

# Prerequistes
*The following steps should be performed in the following order*
1. Disable Raspberry Pi terminal on serial port with raspi-config utility:
    ```bash
    sudo raspi-config
    ```
    Go to ```Interfacing Options``` then choose ```Serial``` then ```NO``` and ```OK```

2. Install pyserial
    ```bash
    sudo apt-get install python-serial
    ```

3. Download scripts
    - if git is installed then clone the repository :
    ```bash
    git clone https://github.com/SNOC/rpisigfox.git
    ```
    - otherwise paste script content to a new file:
    ```bash
    nano sendsigfox.py
    ```

4. Enable script execution
    ```bash
    chmod +x sendsigfox.py
    ```

5. Plug antenna with its cable and send your first message:
    ```bash
    ./sendsigfox.py 0123
    ```

### Pi3 specific requirements
1. Edit ```/boot/config.txt```
      ```bash
      sudo nano /boot/config.txt
      ```
   1. disable if present ```dtoverlay=pi3-miniuart-bt``` by adding ```#``` character at line begining :
   ```#dtoverlay=pi3-miniuart-bt```
   2. if not present, add :
        ```bash
        dtoverlay=pi3-disable-bt
        enable_uart=1
        ```
        *note: ```enable_uart=0``` might be present at the end of the file, in such case it should be commented or modified to ```enable_uart=1```*

2. then reboot :
    ```bash
    sudo reboot
    ```
Serial port to use is the script's default one : ```/dev/ttyAMA0```

##### License

MIT License / read license.txt

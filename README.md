# CopterDrone
This is a 4th semester project from 4 IT engineering students

## Preparing Drone for project files
1. Go to https://www.raspberrypi.org/downloads/raspbian/ and download the latest Raspbian for RPi.
2. Extract downloaded image using 7-zip or similar. You will have an IMG file when done.
3. Download Etcher from https://etcher.io and use it to flash the SD-card.
4. After Raspbian has been flashed to the SD-card, go to the drive on your computer
5. In the SD-drive, create a new empty file called "ssh", and a file called wpa_supplicant.conf.
6. Edit wpa_supplicant.conf with the changes from the below guide "Wifi guide" to make it connect to wifi after initial setup.
7. Insert SD-card into RPi and power it up.

NOTE: Username "pi" and password "raspberry".

## Commmands to run after installing Raspbian
1. sudo apt-get update (takes up to 5 minutes)
2. sudo raspi-config
    1. In the utility, select “Advanced Options”
    2. Set “Serial” to disable OS use of the serial connection
    3. Reboot RPi

## Setup WIFI on RPi
1. sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```
network={
  ssid="drone"
  psk="12345678"
  priority=1
}

network={
  ssid="SDU-GUEST"
  key_mgmt=NONE
  priority=2
}
```
2. sudo nano /etc/network/interfaces
```
auto lo
iface lo inet loopback
iface eth0 inet dhcp

allow-hotplug wlan0
auto wlan0

iface wlan0 inet dhcp
wpa-ssid "SDU-GUEST"
```
## Install NPM, Node and Node-JS
In order for the project to be able to run, we need Node-JS. Run these commands to install it.
```
sudo apt-get install npm
sudo apt-get install node
sudo apt-get install nodejs
```
## Setup Python and Mavlink
1. sudo apt-get install screen python-wxgtk2.8 python-matplotlib python-opencv python-pip python-numpy python-dev libxml2-dev libxslt-dev python-lxml
2. sudo pip install future
3. sudo pip install pymavlink
4. sudo pip install mavproxy

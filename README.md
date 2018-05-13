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

## Commands to run after installing Raspbian
<details>
    <summary><b>Initial setup</b></summary>
Commands to run:
    
```
sudo apt-get update (takes up to 5 minutes)
sudo raspi-config
```

<ol>
    <li>In the raspi-config utility, select “Advanced Options”</li>
    <li>Set “Serial” to disable OS use of the serial connection</li>
    <li>Reboot RPi</li>
</ol>
</details>

<details>
    <summary><b>WiFi setup on RPi</b></summary>
    <b>Files to change:</b>
    
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

</details>

<details><summary><b>Install NPM, Node, Node-JS, and Python</b></summary>
In order for the project to be able to run, we need Node-JS. Run these commands to install it.
    
```
sudo apt-get install npm
sudo apt-get install node
sudo apt-get install nodejs
sudo npm install -g express

For npm in node.js please install:
npm install fs
npm install events
npm install bodyparser
npm install child_process
npm install path
npm install querystring

For python:
pip install dronekit
pip install dronekit_sitl
```
</details>
<details>
    <summary><b>Make node.js file a service on startup</b></summary>
In order to make the node.js file into a service (that will start on startup), the following needs to be done
    1. copy the file drone.service into /etc/systemd/system/
    2. do the following commands:

```
sudo chmod 644 /etc/systemd/system/drone.service
```
</details>
<details><summary><b>Setup Python and Mavlink</b></summary>
To prepare the RPi for mavlink communication, run these commands:
    
```
sudo apt-get install screen python-wxgtk2.8 python-matplotlib python-opencv python-pip python-numpy python-dev libxml2-dev libxslt-dev python-lxml
sudo pip install future
sudo pip install pymavlink
sudo pip install mavproxy
```
</details>

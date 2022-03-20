% Installing HAB Raspberry Pi

# Installing Base system
## Installing Raspberry Pi Lite Image (Buster)
  - [Raspberry Pi Lite](https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2022-01-28/2022-01-28-raspios-bullseye-armhf-lite.zip)
  - Install image on Micro SD Card
  - Create an empty file 'ssh' on the 'boot' partition

## Disable onboard sound system
  - Make the following changes to config.txt on the 'boot' partition
  - Comment the following lines
```
    #Disable audio (loads snd_bcm2835)
    #dtparam=audio=on

    #Disable 
    #dtoverlay=vc4-fkms-v3d
    #dtoverlay=audioinjector-wm8731-audio
```

## Installing Sound Card (WM8731 Codec) (Only if you're building a system with the HAMPiHat board)
  - Make the following changes to config.txt on the 'boot' partition
  - Uncomment or add the following lines
```
    # Enable WM8731 codec
    dtparam=i2c_arm=on
    dtparam=i2s=on
    dtoverlay=i2s-mmap
    dtoverlay=rpi-proto
```

## Create Alsa Sound Config file
  - Create a file './.asoundrc' in '/home/pi' containing the following
  - update 'card' number to point to the right sound card. (use output of 'aplay -l' for the card numbers)
```
pcm.!default {
        type hw
        card 1
}

ctl.!default {
        type hw           
        card 1
}
```
  - This will make the desired soundcard the default

## Tools to check Sound Card functionality
  - apt install alsaplayer-text
  - This can be used to play an audio file to verify sound card functionality


# HAB System
## Direwolf
### Install
 - sudo apt install direwolf

### Config file (Lab setup)
```
< todo: copy default direwolf.config file into this file>
```

### Config file (Ballon setup)
- This config file myst be tailored for use in the balloon


## Python
### Python packets on base system
 - apt install python3-venv

### Python Virtual environment
Instead of installing packages on the base system itself, Python provides a way to install it in
a virtual environment system (VENV). This separates project/program specific Python modules from the base
system. All required python packages are listed in a text file and a helper script checks if it's changed
and updates/installs it when necessary.

#### Python modules
- python-periphery
  - python-periphery is a pure Python library for GPIO, LED, PWM, SPI, I2C, MMIO, and Serial peripheral I/O interface access in userspace Linux. It's not build upon Raspberry Pi specifics and thereby do not have RPi inspired limitation.
  - This module is used to control the GPIO.

- 

Installing python in a venv environment
 - Direwolf provides a KISS interfaces. 




## HAB application
There are several ways to install the HAB application on the Target machine.

- During Development
  - `git clone git+ssh://<username>@<hostname or IP address>:<path to repository on host machine>`

- Deploying
  - Download zip file
  - Extract
  - Run at least the setup part so that all required python modules get installed.
# HAB information and useful links
[ High Altitude Balloon ](https://www.instructables.com/SSTV-CAPSULE-FOR-HIGH-ALTITUDE-BALLOONS/)


# Firmware
## Tiny Core Linux
	http://www.tinycorelinux.net/
	Tiny Core Linux runs entirely from RAM. All packages are loaded at boot time and storage is used read-only. This creates a high resilience against filesystem corruption at power loss. Very useful for battery powered systems.
	
### Packaging application
	<to be filled in>

### Packages to be added for HAB
	<to be filled in>

# Python (and virtual environment)
	Version 3
	Virtual environment
		sudo apt install python3-venv
	https://realpython.com/python-virtual-environments-a-primer/
	https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
	https://approximateengineering.org/2017/04/running-python-as-a-linux-service/
	https://pyserial.readthedocs.io/en/latest/shortintro.html#opening-serial-ports


## Packages
	pip3 install pyserial
	pip3 install pynmea2

### example usages
	https://fishandwhistle.net/post/2016/using-pyserial-pynmea2-and-raspberry-pi-to-log-nmea-output/

# Direwolf
	[Direwolf info](https://packet-radio.net/direwolf/)
	[Direwolf on Raspberry Pi](https://github.com/wb2osz/direwolf/blob/master/doc/Raspberry-Pi-APRS.pdf)
	[Direwolf user guide](https://github.com/wb2osz/direwolf/blob/master/doc/User-Guide.pdf)
	[ Direwolf manual ](https://packet-radio.net/wp-content/uploads/2018/10/Direwolf-User-Guide.pdf)

# GPSD
	https://en.wikipedia.org/wiki/Gpsd
	https://gpsd.gitlab.io/gpsd/index.html

	Abstracting GPS via GSPD allows using the GPS for other firmware components besides Direwolf exclusive usage
	e.g. 
		- Time Sync at (re-)boot. 
		- Logging GPS info in log file (e.g. altitude, horizontal speed, total speed, Location)

# GPS
## Device 
	Datasheet: https://cdn-shop.adafruit.com/datasheets/GlobalTop-FGPMMOPA6H-Datasheet-V0A.pdf

## Documentation
	https://www.gpsinformation.org/dale/nmea.htm#nmea


# GPIO
## Controlling GPIO
	~https://opensource.com/article/17/3/operate-relays-control-gpio-pins-raspberry-pi (PHP)~
	https://www.raspberrypi.org/documentation/usage/gpio/
	https://www.raspberrypi.org/documentation/usage/gpio/python/README.md
		https://pypi.org/project/pigpio/

## Serial Ports
	Raspberry Pi has only 1 serial port. 

### SC16SI752
	[Dual UART with I²C-Bus/SPI Interface](https://www.nxp.com/products/peripherals-and-logic/signal-chain/bridges/dual-uart-with-ic-bus-spi-interface-64-bs-of-transmit-and-receive-fifos-irda-sir-built-in-support:SC16IS752_SC16IS762)
	https://github.com/aauer1/RPI-RS232 (SPI connection)

#### Waveshare I2C SC16SI752 expanders
- Add following line to config.txt
  dtoverlay=sc16is752-i2c,int_pin=24,addr=0x48

#### Linux Kernel
	Raspberry Pi contains device tree overlays for this chip. with programmable I2C addresses and dedicated interrupt line.
	<add info here>

# Logging 
	https://realpython.com/python-logging/
	https://docs.python.org/3.6/library/logging.html#
	https://docs.python.org/3.6/howto/logging-cookbook.html#formatting-styles

# Radio
## AF Radio
	http://thathamkid.com/blog/archives/category/radio (off line at last check)

## Radio module DRA818
	http://www.dorji.com/docs/data/DRA818U.pdf

	Known under different part numbers. All do share the same requirements.
	- analog AF interface for sending and recieving
	- serial interface for configuring radio


## APRS device
	http://www.picoaprs.de/index_en.html 
		- Pico APRS module with own GPS and APRS modem. 
		- Provides KISS interface (interfacing with DireWolf possible?)
		- Used as backup locator beacon besides HAB payload for location/recovery.

# Audio (sound card)
	The raspberry Pi on board audio is audio out only.

## WM8731 (I2S sound device)
	Sound chip that provides:
	- Stereo line in
	- Stereo line out
	- Stereo headphone out
	- Mono microphone in
	Supported in Linux

### Interfacing
	- https://github.com/skiselev/i2s_audio_phat

### Driver
	- https://raspberrypi.stackexchange.com/questions/70614/audio-injector-codec-board-wm8731-bcm2835-i2s-20203000-i2s-i2s-sync-error-rasp#70665

### Splitting Audio in and outputs into individual Mono in and outputs
https://bootlin.com/blog/audio-multi-channel-routing-and-mixing-using-alsalib/

### information on how to configure ALSA
https://alsa.opensrc.org/Asoundrc#What_is_a_.asoundrc_file.3F_Why_might_I_want_one.3F

### Alternative is using ALSA DMIX
https://alsa.opensrc.org/Dmix

# UPS/Power supply
## UPS Pico
	https://pimodules.com/ups-pico-hv4-0b

## Joy-it StromPi V3
	https://joy-it.net/en/products/rb-strompi3
	- LiFe Battery (expected to perform better at low temperature)


# Hardware
## Oscilator
[ Oscilator debugging ](https://www.nxp.com/docs/en/application-note/AN3208.pdf)

## Radio modules
[ HAMRadioShop (Poland) ](https://www.hamradioshop.pl/pl/kity-radiowe-moduly/modul-nadawczo-odbiorczy-dra818v-na-pasmo-vhf-detail.html)
[ HAM Radio (Slovenia) ](https://english.svet-el.si/)



# Tips and Tricks
## GIT
### Git clone over ssh
  e.g. git clone ssh://jan@192.168.1.64:/home/jan/projects/HAM-HAB/HABPiHAT/.git
  ! git push to be done to a non-bare repo will not succeed if the branch you want to push is checked out on remote

## Direwolf
- [ Example Direwolf config ](https://godseyonline.net/raspberry-pi-direwolf-digipeater-igate-soundcard-version/)
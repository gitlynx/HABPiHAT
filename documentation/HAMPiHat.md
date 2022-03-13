# HAM Pi Hat installation and configuration information

# References and links
- [ Raspberry Pi config.txt information ](https://www.raspberrypi.com/documentation/computers/config_txt.html)
- [ DiGi Pi](https://elekitsorparts.com/product/digi-pi-raspberry-pi-hat-ham-radio-digital-modes-ham-radio-remote)
  - Comes with schematic (see Note 5)

# Devices and peripherals
## Disable HDMI
- Not used, but useful if it will conserve some power
- Information is not conclusive on how to do that.
  - Seeking an option in /boot/config.txt

## Serial interfaces
- [ Waveshare reference design ](https://www.waveshare.com/serial-expansion-hat.htm)
  - [ Wiki ](https://www.waveshare.com/wiki/Serial_Expansion_HAT)
- HAM Pi Hat config lines
  - dtoverlay=sc16is752-i2c,int_pin=25,addr=0x4E
    - Serial A
      - Device name: /dev/ttySC2
      - Peripheral: External Serial Port A (labels SerA_tx and SerB_rx)
    - Serial B
      - Device name: /dev/ttySC3
      - Peripheral: External Serial Port B (labels SerB_tx and SerB_rx)
    - GPIO
      - gpiochip496 -> ../../devices/platform/soc/3f804000.i2c/i2c-1/1-004e/gpio/gpiochip496
      - /dev/gpiochip2
  - dtoverlay=sc16is752-i2c,int_pin=24,addr=0x4F
    - Serial A
      - Device name: /dev/ttySC0
      - Peripheral: GPS
    - Serial B
      - Device name: /dev/ttySC1
      - Peripheral: DRA818 (Radio)
    - GPIO
      - ../../devices/platform/soc/3f804000.i2c/i2c-1/1-004f/gpio/gpiochip504
      - /dev/gpiochip1
- Python
  - https://pyserial.readthedocs.io/en/latest/pyserial_api.html


### configuration
- Add the following to /boot/config.txt
  - dtoverlay=sc16is752-i2c,int_pin=24,addr=48 
  - Update int_pin and addr to match your situation

## GPIO
Python Library
- https://python-periphery.readthedocs.io/en/latest/gpio.html#code-example
- https://duckduckgo.com/?t=ffab&q=sysfs+gpio+python&atb=v290-1&ia=web
- https://embeddedbits.org/new-linux-kernel-gpio-user-space-interface/

>>> hl = periphery.GPIO("/dev/gpiochip2", 2, "out")
>>> hl.read()
True
>>> hl.write(True)
>>> enable = periphery.GPIO("/dev/gpiochip1", 3, "out")
>>> enable.read()
True
>>> enable.write(True)


C Library
- https://elinux.org/C
- https://microhobby.com.br/blog/2020/02/02/new-linux-kernel-5-5-new-interfaces-in-gpiolib/



## Sound
### Links and references
- [ Mikroe-506 Schematic ](https://download.mikroe.com/documents/add-on-boards/click/audio-codec-proto-board/Audio%20Codec%20Board%20-%20PROTO_v102_Schematic.PDF)
- https://learn.adafruit.com/usb-audio-cards-with-a-raspberry-pi/updating-alsa-config
- https://www.alsa-project.org/main/index.php/Asoundrc
  - Be aware. Might contain an error (see https://forums.raspberrypi.com/viewtopic.php?t=175233 that mention it)
- [ WM8731 I2C address ](https://www.kernel.org/doc/Documentation/devicetree/bindings/sound/wm8731.txt)
### Hardware
- Disable Rpi sound card
  - Put following line in comment in /boot/config.txt
```
    # Enable audio (loads snd_bcm2835)
    #dtparam=audio=on
```

- Enable/configure WM8731 based card
  - Add following lines to /boot/config.txt
    ```
    # Enable WM8731 codec
    dtparam=i2c_arm=on
    dtparam=i2s=on
    dtoverlay=i2s-mmap
    dtoverlay=rpi-proto
    ```
  - See [ I2C Audio HAT ](https://github.com/skiselev/i2s_audio_phat)
    - Read instruction to enable mixer output !!

### PulseAudio
!! Remove from system as it interferes with desired operation

### Alsa
- Alsa card name is the name in brackets found in /proc/asound/cards 
  - See https://james.ahlstrom.name/alsa_names.html
- How to find card name
  - See https://unix.stackexchange.com/questions/627275/how-to-find-the-id-of-an-alsa-capture-device-by-name
    Card indexes may change.


#### AlsaMixer
#### Configure all channels as individual mono channels
- [ Audio multi channel routing and mixing ](https://bootlin.com/blog/audio-multi-channel-routing-and-mixing-using-alsalib/)
- Working asoundrc file available [here](./asoundrc)
  - Audio device is available under the alias 'hat'
  - output 'out0' is single mono output channel
    - Left channel
    - e.g. alsaplayer -d out0 Chiptronical.ogg
  - output 'out1' is single mono output channel
    - Right channel
    - e.g. alsaplayer -d out1 Interplanetary\ Odyssey.ogg 


#### CLI constrol over Alsa mixer
- [ Sound configuration and control on RPi with Alsa ](http://blog.scphillips.com/posts/2013/01/sound-configuration-on-raspberry-pi-with-alsa/)

#### Python Control over Alsa devices
##### AlsaAudio
- [ Alsaaudio ](https://pypi.org/project/pyalsaaudio/)
- [ Example python ](https://gist.github.com/ubershmekel/6626065)
- [ Example python ](https://www.programcreek.com/python/example/91452/alsaaudio.Mixer)
- Works. Now to find out how to fine control left and right separately

### Tools and programs
#### playing/recording sound files
- aplay records and plays files 
    (wav files)
- alsaplayer
    (Plays encoded files)

# GPS
## Links and references
- [ GPSD ](https://gpsd.io/)

## GPSD
Package: gpsd
- (Linux) Daemon that makes gps avialable for multiple clients. See 'man gpsd' for details
- Listens standard on local loopback only. Unless '-G' argument is added.
- Standard daemonizes unless '-N' argument is added. Usefull for testing and debugging error situations
- Defaults listens on TCP/IP port 2947
- Sample commandline on Raspberry Pi (with USB connected PhotoTrackr GPS device)
  - gpsd -N /dev/ttyACM0
  - !! Package installed and gpsd got started automatically
    - Is added to Raspbian start scripts with start-stop-daemon and in /etc/rc.x and /etc/init.d
    - Default settings can be set in file /etc/default/gpsd (rapsbian)
- GPS time is in UTC.
  - Either being converted to local time or used in UTC. (prefer the lather) 


Package: gpsd-clients
- applications: 
  - /usr/bin/cgps --> console tool showing raw and decode GPS information
  - /usr/bin/gegps
  - /usr/bin/gps2udp
  - /usr/bin/gpscat
  - /usr/bin/gpsctl
  - /usr/bin/gpsdecode
  - /usr/bin/gpsfake
  - /usr/bin/gpsmon --> usefull too to debug. Can use gpsd socket or direct access
  - /usr/bin/gpspipe
  - /usr/bin/gpsprof
  - /usr/bin/gpsrinex
  - /usr/bin/gpxlogger
  - /usr/bin/lcdgps
  - /usr/bin/ntpshmmon
  - /usr/bin/ubxtool
  - /usr/bin/xgps
  - /usr/bin/xgpsspeed
  - /usr/bin/zerk

  ### Python Interface
  - [ GPS3 ](https://pypi.org/project/gps3/)
    - pip install gps3
  - Example code works with gpsd and multiple clients.
    - Python interface works. 

# Direwolf
- [ Direwolf Documentation ](https://github.com/wb2osz/direwolf/tree/master/doc)
  - [ Direwolf Presentation ](https://github.com/wb2osz/direwolf-presentation)
- [ Direwolf Packet Radio ](https://packet-radio.net/direwolf/)
- [ Direwolf Release ](https://packet-radio.net/direwolf-1-6-official-release/)
- [ Direwolf APR Youtube Video ](https://www.youtube.com/watch?v=o34l9mSxWys)
- [ FE-PI sound bonnet for APRS ](https://www.youtube.com/watch?v=JyGBscgtXxg)
- [ How to send telemetry with Direwolf ](https://github.com/wb2osz/direwolf/blob/master/doc/APRS-Telemetry-Toolkit.pdf_)
- [ Direwolf Digipeater Igate (Entry Level)](https://k5eok.org/2021/01/19/aprs-digipeater-igate-with-direwolf-entry-level/)
- [ APRS Telemetry ](https://groups.io/g/direwolf/topic/72038666)
- [ APRS Direct ](https://www.aprsdirect.com/) Website builder

## Extra's
- [ APRS telemetry watcher ](https://aprstw.blandranch.net/)  (from 2012)
  - [Windows Sound Card Packet](https://www.soundcardpacket.org/) (sound card interface for windows) (from 2013)
- [ Yet Another APRS Client (YAAC) ](https://www.ka2ddo.org/)
  - [ Install on RPi instruction video](https://www.youtube.com/watch?v=94mIEBVhsLY)
  - [ Install it on Ubuntu and work with Direwolf ](https://www.youtube.com/watch?v=4tEWIIqhLN0)
- [ Raspberry Pi Pico High Altitude Ballooon ](https://www.raspberrypi.com/news/raspberry-pi-pico-balloon-tracker/)


## Known working combinations
- [ FE-Pi ](https://pinout.xyz/pinout/fe_pi_audio_z_v2#)

## Config file
- [ Example config file (Not matching our setup) ](https://github.com/elafargue/aprs-box/blob/master/config/etc/direwolf/direwolf.conf)

## Observations
- Uses 15-20% cpu time op 1 core.
- Enable BEACON line(s) in config to send out baecon reports in regular interval. Without it's completely silent.
- Direwolf 'adevice' in config file --> claims complete audio device
  - start/stop direwolf to enable other transmission types?
  - Is there an option to share audio device?
    - [ Direwolf Forum ](https://groups.io/g/direwolf/topic/79112202)

## Development setup
With a tranceiver attached you broadcast everything publickly withing the radio coverage of your setup. This is not handy when you're developping and other will not appreciate you spamming the ether the whole time. Luckily it's possible to create a send and receive setup without the radio part. Just connect 2 Direwolf instances.

The raspberry Pi only has a speaker/headphone out. But that's quickly solved by adding an USB sound interface. Connect the speaker/headphone out of the Raspberry Pi to the microphone in on the USB sound interface on the second Raspberry Pi.

It's possible to condense the entire setup to 1 Raspberry Pi by using 2 separate direwolf config files. Each pointing to a different audio device. (not testes, but assume this must work)

## Python interface
### Kiss
- [ kiss module ](https://pypi.org/project/kiss/)
  - For TCP connection use kiss.TCPKISS(<host>, <port>)
  - Multiple KISS clients can connect to DireWolf
- [ KISS2 module](https://gitlab.scd31.com/stephen/kiss2)
  - Above kiss module is claimed no longer being maintained

### APRS
- [ APRS module ](https://github.com/ampledata/aprs)
  - Is APRS-IS: APRS-Internet Service. Looks to be more the Internet side of it. Not for the RF part
- [ APRS-python](https://github.com/jj1bdx/aprs-python) <---------------------------
  - Is Fork of above library with added TCPKISS functionality
  - [ Instruction on how to install ](https://www.geeksforgeeks.org/how-to-install-python-libraries-without-using-the-pip-command/)
  - pip3 install git+https://github.com/jj1bdx/aprs-python
  - [ Installing python lib from github ](https://pypi.org/project/aprslib/) See example on that page
  - Last work on it is done 5 years a go. Not up to date with recent python version

- [ APRS Standard 1.0(pdf)](http://www.aprs.org/doc/APRS101.PDF)
  - [ APRS Addemdum 1.1](http://www.aprs.org/aprs11.html)
  - [ APRS Protocol version 1.2 (proposal)](http://www.aprs.org/aprs12.html)
- [ APRS Documentation](http://www.dididahdahdidit.com/dosaprs.php)
- [ APRS SSID extra information](http://www.aprs.org/aprs11/SSIDs.txt)
- [ Direwolf and APRS on Reddit ](https://www.reddit.com/r/amateurradio/comments/7brjjj/producing_aprs_packets_in_python_for_direwolf/)


### Telemetry
Turning the whole setup upside down.
Running a script from Direwolf to retrieve information from the logging system
see [ webpage ](https://0x9900.com/aprs-telemetry/)

#### Side projects
- [ APRS-Pi ](https://kandi.openweaver.com/python/ThreeSixes/aprs-pi) Seems to be Rx only, interfacing between MQT and APRS and no details about encoding.
- [ Arduino APRS implementation ](https://handiko.github.io/Arduino-APRS/)
  - [ Software ](https://github.com/handiko/Arduino-APRS)


# Power reduction
## HDMI
- [ -20mA ] 'tvservice -o' turns off HDMI.

## Ethernet
- [ -30mA ] Disconnect Ethernet cable 
- !! Final board will not have ethernet or USB hub

with above changes --> 0.2A on Raspberry Pi 3B+ 


# SSTV
References
[ SSTV Handbook ](https://sstv-handbook.com/)
[ SSTV tool on RPi ](https://km4nmp.com/2019/11/24/sstv-with-the-raspberry-pi-4b/)
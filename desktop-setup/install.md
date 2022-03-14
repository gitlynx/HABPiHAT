% Balloon Desktop Setup

# Installing the balloon device
## Linux Base Image install
- Starting from a Raspberry Pi Lite image. Write it to a micro SD card
- Enable ssh
  - create an empty file with name 'ssh' in the /boot directory on the micro SD card
- Boot the Raspberry Pi with this micro SD card

## Update Raspberry Pi image
- sudo apt update
- sudo apt upgrade

## Setting up/checking audio
- Plug in an USB audio dongle. The onboard audio card is missing the recording option. Direwolf complains about it and refuses to start.
    - Have the line/headphone out connected to headphones or speakers
- Run speaker-test
  - This will generate some audio patterns.

## install an asound.conf file
This file defines the USB audio dongle as default. 

## Installing project specific tools and programs
### Direwolf
#### References
[ Direwolf website ](https://packet-radio.net/direwolf/)
[ Direwolf Github ](https://github.com/wb2osz/direwolf)
[ Direwolf manual ](https://packet-radio.net/wp-content/uploads/2018/10/Direwolf-User-Guide.pdf)
[ Retrieving telemetry via a script ](https://0x9900.com/aprs-telemetry/)

### APRS
[ APRS instruction ](http://www.w8qqq.org/docs/APRS_DP1.pdf)
[ APRS protocol specification ](http://www.aprs.org/doc/APRS101.PDF)
[ APRS telemetry explained ](https://github.com/PhirePhly/aprs_notes/blob/master/telemetry_format.md)
[ APRS telemetry toolkit ](https://raw.githubusercontent.com/wb2osz/direwolf/master/doc/APRS-Telemetry-Toolkit.pdf) Legacy format and BASE91 encoded.
[ APRS telemetry example ](https://w4krl.com/sending-aprs-analog-telemetry-the-basics/)
[ Example Direwolf config file ](https://gist.github.com/tedwardd/705fdd42f5762554a21d0ffd8812c259)
[ Install Direwolf on Raspberry Pi ](https://www.marrold.co.uk/2019/04/installing-direwolf-15-on-raspberry-pi.html)
  - This is with an USB audio device

#### Installing
- sudo apt install direwolf

Install direwolf config file
- 



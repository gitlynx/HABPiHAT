# HAM Pi Hat installation and configuration information

# References and links
- [ Raspberry Pi config.txt information ](https://www.raspberrypi.com/documentation/computers/config_txt.html)


# Devices and peripherals
## Disable HDMI
- Not used, but useful if it will conserve some power
- Information is not conclusive on how to do that.
  - Seeking an option in /boot/config.txt

## Sound
### Links and references
- https://learn.adafruit.com/usb-audio-cards-with-a-raspberry-pi/updating-alsa-config
- https://www.alsa-project.org/main/index.php/Asoundrc
  - Be aware. Might contain an error (see https://forums.raspberrypi.com/viewtopic.php?t=175233 that mention it)
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

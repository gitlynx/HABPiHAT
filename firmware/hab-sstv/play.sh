#!/usr/bin/env bash

if [ -f /tmp/latest.wav ]; then
	aplay -D plughw:CARD=Device,DEV=0 /tmp/latest.wav
fi


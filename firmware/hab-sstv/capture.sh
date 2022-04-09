#!/usr/bin/env bash

#
#  Capture an image from the camera in High Ress
#  Add Exif data to image
#
#  Convert image (scale) to SSTV Robot36 format
#
#
#

# Shell config

SSTVFOLDER="/tmp/"

#########################################
## DO NOT MAKE CHANGES BELOW THIS LINE ##

# Shell script options 
set -e

# Constants
# #####################################
SPACE=" "

# Configuration
# #####################################A
LOGFILE="sstv.log"

WIDTH=0
HEIGHT=0

LATEST_FILE="latest.jpeg"
LATEST_SSTV="sstv.jpeg"

capture_high_res()
{
	local filename=$1
	local storedir=$(dirname $1)

	echo "\n\t$storedir\n\n"

	IMAGE_OPTION="--width ${WIDTH} --height ${HEIGHT}"
	FILENAME="-o $1"
	LATEST="--latest ${SSTVFOLDER}${LATEST_FILE}"
	EXIF="--exif GPS.GPSLatitude=51.111"


	libcamera-still -t 10000 -n ${IMAGE_OPTIONS} ${FILENAME} ${LATEST} ${EXIF} 
}

add_exif_info()
{
	# Latest image can be found via the symlink
	#  Use this to
	:
}

convert_to_sstv()
{
	local _text=("ON4NOK" "$1")
	local text="\"${_text[@]}\""

	echo "Convert to SSTV format"
	echo "text: $text"
	echo "arg 1: $1"

	# Common options
	INPUT_FILE=${SSTVFOLDER}${LATEST_FILE}
	OUTPUT_FILE=${SSTVFOLDER}${LATEST_SSTV}

	# Resize
	#   Robot 36 mode accepts an image 320x240 (4:3-format)
        #
	#   Resize:  "-resize 320x240"
	#
	# Add color bar
	#   Color Bar:  -stroke black -draw "rectangle 0,210,320,240\"
	#
	# Add Text
	#   Text: -fill white -draw "text <location x y> <text>

	convert ${INPUT_FILE} \
		-resize 320x240 \
		-stroke black -draw "rectangle 0,210,320,240" \
		-fill white -antialias \
		-pointsize 32 \
		-stroke none -draw "text 10,235 ${text[@]}" \
		$OUTPUT_FILE
}

add_to_log()
{
	local logfile=$1
	local altitude=$2
	
	echo "Add to LOG"
	# Real Filename
	imagefile=$(basename $(readlink ${SSTVFOLDER}/latest.jpeg))

	# Add newest conversion to log file
	if [ ! -e ${SSTVFOLDER} ] ; then
		mkdir -p ${SSTVFOLDER}
	fi

	echo "${imagefile}:${altitude}" >> ${SSTVFOLDER}${LOGFILE}
}

convert_to_wav()
{
	# Convert latest image to wave file
	echo "Converting to WAV"
}


# Main part of script
ALTITUDE="${1} m"

echo "ALT: $ALTITUDE"
echo "arg 1: $1"

NAME="./$(date +%Y%m%d%H%M%S).jpeg"
capture_high_res "${SSTVFOLDER}${NAME}"
add_to_log "${SSTVFOLDER}" "${ALTITUDE}"
convert_to_sstv "${ALTITUDE}"
convert_to_wav


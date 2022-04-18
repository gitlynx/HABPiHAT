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

SSTVFOLDER="/home/pi/telemetrydata/sstv/"

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
LATEST_SSTV="sstv.png"

capture_high_res()
{
	local filename=$1
	local storedir=$(dirname $1)

	IMAGE_OPTION="--width ${WIDTH} --height ${HEIGHT}"
	FILENAME="-o $1"
	LATEST="--latest ${SSTVFOLDER}${LATEST_FILE}"


	libcamera-still -t 10000 -n ${IMAGE_OPTIONS} ${FILENAME} ${LATEST}
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
	imagefile=$(basename $(readlink ${SSTVFOLDER}/${LATEST_FILE}))

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

	
	INPUT_SSTV=${SSTVFOLDER}${LATEST_SSTV}
	OUTPUT_WAV=/tmp/latest.wav


	PYTHON_EXEC=${PYTHON_EXEC:-python3}
	VENV_DIR=${VENV_DIR:-venv}

	# Update VENV if it changed or does not exist
	REQUIREMENTS_HASH=$(md5sum requirements.txt)
	EXISTING_REQUIREMENTS_HASH=$(cat ${VENV_DIR}/requirements.md5 2>/dev/null || true)

	if [ ! "${REQUIREMENTS_HASH}" = "${EXISTING_REQUIREMENTS_HASH}" ]; then
		PYTHON_V=$(${PYTHON_EXEC} version-check.py)
		${PYTHON_EXEC} -m venv ${VENV_DIR}
		./${VENV_DIR}/bin/pip install --upgrade pip setuptools
		./${VENV_DIR}/bin/pip install -r requirements.txt
		echo -n "${REQUIREMENTS_HASH}" > ${VENV_DIR}/requirements.md5
	fi

	SSTV_MODE="Robot36"

	CMD="./${VENV_DIR}/bin/python -m pysstv --mode ${SSTV_MODE} ${INPUT_SSTV} ${OUTPUT_WAV}"

	echo "--> ${CMD}"
	exec ${CMD}

}

ALTITUDE="${1} m"

echo "ALT: $ALTITUDE"
echo "arg 1: $1"

NAME="./$(date +%Y%m%d%H%M%S).jpeg"
capture_high_res "${SSTVFOLDER}${NAME}"
add_to_log "${SSTVFOLDER}" "${ALTITUDE}"
convert_to_sstv "${ALTITUDE}"
convert_to_wav


#!/bin/bash

FILES="$@"

for i in $FILES
do
	echo "Processing image $i"
	/usr/bin/convert -thumbnail 1280 $i preview/thumb.$i
done

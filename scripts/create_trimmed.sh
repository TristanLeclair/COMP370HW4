#!/bin/bash

# verify that argument 1 is a file
if [ ! -f "$1" ]; then
    echo "Usage: $0 <file>"
    exit 1
fi

# if argument 2 is not provided, set it to 2020
if [ -z "$2" ]; then
    year=2020
else
    year=$2
fi

# extract filename without extension
filename=$(basename -- "$1")

newfile="$filename.$year.csv"

# create a new file with the trimmed data
grep -P "^\d{8,10},\d{2}/\d{2}/$year" $1 > $newfile

# add headers to new csv file
cat headers.csv > trimmed.csv && cat $newfile >> trimmed.csv
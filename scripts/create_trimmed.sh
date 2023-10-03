#!/bin/bash

Usage="Usage: $0 <data file> <headers file> [<year>]"
# verify that argument 1 is a file
if [ ! -f "$1" ]; then
    echo $Usage
    exit 1
fi

# verify that argument 2 is a file
if [ ! -f "$2" ]; then
    echo $Usage
    exit 1
fi

# if argument 3 is not provided, set it to 2020
if [ -z "$3" ]; then
    year=2020
else
    year=$3
fi

# extract folder from file path
folder=$(dirname -- "$1")

# extract filename without filetype
filename=$(basename -- "$1" | cut -f 1 -d '.') 

newfile="$filename.$year.csv"

# create a new file with the trimmed data
grep -P "^\d{8,10},\d{2}/\d{2}/$year" $1 > $folder/$newfile

# add headers to new csv file
cat $2 > $folder/trimmed.csv && cat $folder/$newfile >> $folder/trimmed.csv

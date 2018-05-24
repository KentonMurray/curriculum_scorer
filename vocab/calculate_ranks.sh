#!/bin/bash

### Run this script on a dataset file. It gives the counts of all words ###

if [ $# -eq 0 ]; then
    echo "No arguments provided"
    echo "Correct Usage: calculate_ranks.sh [file]"
    exit 1
fi

FILE=$1

cat $FILE | awk '{for (i = 1; i <= NF; i++) {print $i}}' | sort | uniq -c | sort -rn

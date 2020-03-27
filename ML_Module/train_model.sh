#!/bin/bash
path=`pwd`

printf "Step 1: Collecting data from Sever.\n"
$path/collect_log.sh 3 600 wlp3s0 

printf "Step 2: Processing training data.\n"
python $path/process_data.py

printf "Step 3: Training the ML model.\n"

#!/bin/bash
path=`pwd`

printf "Step 1: Collecting data from Sever in 60s.\n"
$path/collect_log.sh 3 60 wlp3s0 

printf "Step 2: Processing testing data.\n"
python $path/process_test_data.py 1

printf "Step 2: Test log data with the machince learning model.\n"
 

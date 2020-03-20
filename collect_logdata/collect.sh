#!/bin/bash
printf "Start to collect data every %ds for %ds.\n" "$1" "$2" 
printf "Net device: %s\n" "$3"
let i_step=$1*100/$2
i=0
bar=''
while [ $i -le 100 ]
do
    printf "[%-20s][%d%%]\r" "$bar" "$i"
    let i+=i_step
    bar+='='
    A=`date "+%H:%M:%S"`
    B=`top -b -n 1 | sed -n '2p' | awk '{print $2}'`
    C=`top -b -n 1 | sed -n '3p' | awk '{print $8}'`
    D=`free -m | awk '{print $3}' |sed -n '2p'`
    E=`iostat |sed -n '7p'|awk '{print $3","$4}'`
    F=`cat /proc/net/dev | grep $3 | sed 's/:/ /g' | awk '{print $2","$10}'`
    printf "%s,%s,%s,%s,%s,%s\n" "$A" "$B" "$C" "$D" "$E" "$F">>data1.csv 
    sleep $1
done
uptime | awk '{print $8 $9 $10}' >> cpu_avg.log
printf "\nComplete!\n"


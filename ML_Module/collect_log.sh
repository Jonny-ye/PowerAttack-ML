#!/bin/bash
path=./log_data

printf "tasks,cpu_idle,mem,disk_i,disk_o,net_dn,net_up\n">$path/base_data.log
printf "load_avg_1,load_avg_5,load_avg_15\n">$path/load_avg.log
printf "date_t\n">$path/date_t.log

let len=$2/$1
i=0
t=0

while [ $i -lt $len ]
do
    A=`top -b -n 1 | sed -n '2p' | awk '{print $2}'`
    B=`top -b -n 1 | sed -n '3p' | awk '{print $8}'`
    C=`free -m| awk '{print $3}' |sed -n '2p'`
    D=`iostat |sed -n '7p'|awk '{print $3","$4}'`
    E=`cat /proc/net/dev | grep $3 | sed 's/:/ /g' | awk '{print $2","$10}'`
    printf "%s,%s,%s,%s,%s\n" "$A" "$B" "$C" "$D" "$E">>$path/base_data.log
    let i+=1
    let res=i%20
    if [ $res -eq 0 ];then
        date +%s>>$path/date_t.log
        uptime | awk '{print $8 $9 $10}'>>$path/load_avg.log
    fi
    let t=100*i/len
    printf "Progress: %d%%\r" "$t"
    sleep $1
done
printf "\ncomplete!\n\n"

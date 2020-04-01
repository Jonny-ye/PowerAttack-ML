#!/bin/bash

#***************
#Author: Jonnyye
#Date: 2020.3.31

#参数说明：
#采集总时间：无限制
#网络设备名称
net_tool="wlp3s0"
#日志存储路径
path=./log_data
#采集时间间隔
step_t=3
#***************

#开始采集
while true
do
    A=`uptime|awk '{print $8 $9 $10}'`
    B=`top -b -n 1|sed -n '2p'|awk '{print $2}'`
    C=`top -b -n 1|sed -n '3p'|awk '{print $8}'`
    D=`free -m|awk '{print $3}'|sed -n '2p'`
    E=`iostat|sed -n '7p'|awk '{print $3","$4}'`
    F=`cat /proc/net/dev | grep $net_tool | sed 's/:/ /g' | awk '{print $2","$10}'`
    printf "%s,%s,%s,%s,%s,%s\n" "$A" "$B" "$C" "$D" "$E" "$F" >> $path/base_data.log
    sleep $step_t
done

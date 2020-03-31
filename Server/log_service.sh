#!/bin/bash

#***************
#Author: Jonnyye
#Date: 2020.3.31

#参数说明：
#采集总时间 无限制
#网络设备名称 $1
#日志存储路径
path=./log_data
#采集时间间隔
step_t=3
#***************


#清空日志文件并写入数据项名称
printf "l1,l5,l15,tasks,cpu_idle,mem,disk_i,disk_o,net_dn,net_up\n">$path/base.log   

#计算采集总量
let total=$1/$step_t
while [ $total -le 40 ]
do
    read -p "采集时间过短，请重新输入(>120s):" tmp
    let total=$tmp/$step_t
done
printf "Total:%d\n" "$total"


#开始采集
i=0
while true
do
    A=`uptime|awk '{print $8 $9 $10}'`
    B=`top -b -n 1|sed -n '2p'|awk '{print $2}'`
    C=`top -b -n 1|sed -n '3p'|awk '{print $8}'`
    D=`free -m|awk '{print $3}'|sed -n '2p'`
    E=`iostat|sed -n '7p'|awk '{print $3","$4}'`
    F=`cat /proc/net/dev | grep $2 | sed 's/:/ /g' | awk '{print $2","$10}'`
    printf "%s,%s,%s,%s,%s,%s\n" "$A" "$B" "$C" "$D" "$E" "$F" >> $path/base.log
    let i+=1
    printf "Current:%d\r" "$i"
    sleep $step_t
done
printf "\ncomplete!\n\n"

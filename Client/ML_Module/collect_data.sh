#!/bin/bash

#***************
#Author: Jonny-ye
#Date: 2020.3.31

#参数说明：
#采集总时间 $1
#网络设备名称 
net_device="enp6s0f0"
#硬盘设备名称
disk_device="sda"
#日志存储路径
path=./data
#采集时间间隔(循环中指令时延约2s)
step_t=1
#***************


#清空缓存数据
printf "">$path/time.tmp
printf "">$path/base.tmp

#计算采集总量
let total=$1/$step_t
while [ $total -le 40 ]
do
    read -p "采集时间过短，请重新输入(>120s):" tmp
    let total=$tmp/$step_t
done
printf "Total:%d\n" "$total"

#开始采集数据
i=0
while [ $i -lt $total ]
do
    A=`cat /proc/loadavg | awk '{print $1","$2","$3}'`     #平均负载值
    B=`top -bn 1|sed -n '2p'|awk '{print $2}'`             #进程数量
    C=`sar -u 1 1| grep Average|awk '{print $8}'`          #CPU空闲率(%)
    D=`free -m|awk '{print $3}'|sed -n '2p'`               #内存占用(MB)
    E=`cat /proc/net/dev | grep $net_device | sed 's/:/ /g' | awk '{print $2","$10}'` #网络设备字节计数
    F=`iostat -d| grep $disk_device|awk '{print $3","$4}'`        #硬盘平均读写速度(KB/s)
    G=`ipmitool sdr list |grep Total_Power | awk '{print $3}'`  #ipmitool系统功耗
    echo `date -R`>>$path/time.tmp
    printf "%s,%s,%s,%s,%s,%s,%s\n" "$G" "$A" "$B" "$C" "$D" "$E" "$F" >> $path/base.tmp
    let i+=1
    printf "Current:%d\r" "$i"
    sleep $step_t
done
printf "\ncomplete!\n\n"

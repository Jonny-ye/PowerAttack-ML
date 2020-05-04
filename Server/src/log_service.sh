#!/bin/bash

#***************
#Author: Jonnyye
#Date: 2020.5.3

#参数说明：
#采集总时间：无限制
#网络设备名称
net_device="enp6s0f0"
#磁盘设备名称
disk_device="sda"
#日志存储路径
path=./src/data
#采集时间间隔(循环中指令时延约2s)
step_t=1
#***************

printf "">$path/time.tmp
printf "">$path/base.tmp
#开始采集
while true
do
    A=`cat /proc/loadavg | awk '{print $1","$2","$3}'` #平均负载值
    B=`top -b -n 1|sed -n '2p'|awk '{print $2}'`       #进程数量
    C=`sar -u 1 1|grep Average|awk '{print $8}'`       #CPU空闲率(%)(时延1s)
    D=`free -m|awk '{print $3}'|sed -n '2p'`           #内存占用(MB)
    E=`cat /proc/net/dev | grep $net_device | sed 's/:/ /g' | awk '{print $2","$10}'` #网络设备字节计数 
    F=`iostat -d| grep $disk_device|awk '{print $3","$4}'`       #硬盘平均读写速度(KB/s)
    G=`ipmitool sdr list |grep Total_Power |awk '{print $3}'`   #ipmitool系统功耗
    echo `date -R` >> $path/time.tmp                   #时间
    printf "%s,%s,%s,%s,%s,%s,%s\n" "$G" "$A" "$B" "$C" "$D" "$E" "$F" >> $path/base.tmp
    sleep $step_t
done
 

#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import numpy as np

#处理数据
def process_data(group_n):
    # 打开日志文件
    d = np.loadtxt("./data/base.tmp",delimiter = ',',skiprows=1)
    # 计算数据组数
    t = int(len(d)/group_n)
    
    for i in range(len(d)):
        d[i][5] = round(100 - d[i][5],2)  #CPU空闲率转化为占用率
        d[i][7] = round(d[i][7]/1024,2)  #网络设备字节计数B转化为KB
        d[i][8] = round(d[i][8]/1024,2)
        
    tmp = []
    for i in range(t):
        s = i*group_n  #组开始行数
        e = s+group_n  #组结束行数
        
        s_watts_avg,s_watts_max = d[s][0],d[s][0]
        load15,load5,load1 = d[e-1][1],d[e-1][2],d[e-1][3]
        t_ms = d[s+1][4]-d[s][4]
        c_avg,c_max,c_ms = d[s][5],d[s][5],d[s+1][5]-d[s][5]
        m_avg,m_max,m_ms = d[s][6],d[s][6],d[s+1][6]-d[s][6]
        ni_ms,no_ms = d[s+1][7]-d[s][7],d[s+1][8]-d[s][8]
        di_max,do_max = d[s][9],d[s][10]
        
        for j in range(s+1,e):
            s_watts_avg += d[j][0]
            if s_watts_max < d[j][0]:
                s_watts_max = d[j][0];
            if t_ms < d[j][4]-d[j-1][4]:
                t_ms = d[j][4]-d[j-1][4]
            c_avg += d[j][5]
            if c_max < d[j][5]:
                c_max = d[j][5]
            if c_ms < d[j][5]-d[j-1][5]:
                c_ms = d[j][5]-d[j-1][5]
            m_avg += d[j][6]
            if m_max < d[j][6]:
                m_max = d[j][6]
            if m_ms < d[j][6]-d[j-1][6]:
                m_ms = d[j][6]-d[j-1][6]
            if ni_ms < d[j][7]-d[j-1][7]:
                ni_ms = d[j][7]-d[j-1][7]
            if no_ms < d[j][8]-d[j-1][8]:
                no_ms = d[j][8]-d[j-1][8]
            if di_max < d[j][9]:
                di_max = d[j][9]
            if di_max < d[j][10]:
                do_max = d[j][10]
        
        # 组内数值均值计算    
        s_watts_avg /= group_n 
        c_avg /= group_n
        m_avg /= group_n
        
        #生成一个样本数据
        tmp.append([s_watts_avg,s_watts_max,load15,load5,load1,t_ms,c_avg,c_max,c_ms,m_avg,m_max,m_ms,ni_ms,no_ms,di_max,do_max])
        
    np.set_printoptions(suppress=True)
    np.savetxt("./train_data/train_tmp.csv",tmp,fmt='%.2f',delimiter = ',')

#采用极值归一化
def normalize_data():
    data = np.loadtxt("./train_data/train_tmp.csv", delimiter=',')
    rows = len(data)
    cols = len(data[0])
    max_x = [0]*cols
    
    # 生成最大值数组
    for i in range(rows):
        for j in range(cols):
            if max_x[j]<data[i][j]:
                max_x[j] = data[i][j]
    # 每个样本归一化
    for i in range(rows):
        for j in range(cols):
            if max_x[j] != 0:
                data[i][j] /= max_x[j]
            else:
                data[i][j] = 1.0
                
    # 保存最大值数组和归一化样本数据
    np.savetxt("./train_data/max_x.csv",max_x,fmt='%.4f',delimiter=',')
    np.savetxt("./train_data/train_x.csv",data,fmt='%.4f',delimiter=',')

def main():
    #预处理数据
    process_data(10)
    #归一化数据
    normalize_data()
    print("complete!\n")
    
if __name__=='__main__':
    main()

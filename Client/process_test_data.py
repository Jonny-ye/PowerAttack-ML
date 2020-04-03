#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import numpy as np
import sys

#处理数据
def process_data(group_n):
    d = np.loadtxt("./test_data/base_data.log",delimiter = ',')
    e = len(d)
    s = e - group_n
    if s < 0:
        s=0
    
    for i in range(s,e):
        d[i][4] = 100 - d[i][4]
        d[i][6] /= 1024
        d[i][7] /= 1024
    
    tms = d[s+1][3]-d[s][3]
    c_avg,cmax,cmin,cms = d[s][4],d[s][4],d[s][4],d[s+1][4]-d[s][4]
    m_avg,mmin,mmax,mms = d[s][5],d[s][5],d[s][5],d[s+1][5]-d[s][5]
    ni_avg,no_avg = d[s+1][6]-d[s][6],d[s+1][7]-d[s][7]
    di_avg,do_avg = d[s][8],d[s][9]
    
    for j in range(s+1,e):
        if tms < d[j][3]-d[j-1][3]:
            tms = d[j][3]-d[j-1][3]
        c_avg += d[j][4]
        if cmin > d[j][4]:
            cmin = d[j][4]
        if cmax < d[j][4]:
            cmax = d[j][4]
        if cms < d[j][4]-d[j-1][4]:
            cms = d[j][4]-d[j-1][4]
        m_avg += d[j][5]
        if mmin > d[j][5]:
            mmin = d[j][5]
        if mmax < d[j][5]:
            mmax = d[j][5]
        if mms < d[j][5]-d[j-1][5]:
            mms = d[j][5]-d[j-1][5]
        if ni_avg < d[j][6]-d[j-1][6]:
            ni_avg = d[j][6]-d[j-1][6]
        if no_avg < d[j][7]-d[j-1][7]:
            no_avg = d[j][7]-d[j-1][7]
        di_avg += d[j][8]
        do_avg += d[j][9]
        
    c_avg /= group_n
    m_avg /= group_n
    di_avg /= group_n
    do_avg /= group_n
    tmp = [d[e-1][0],d[e-1][1],d[e-1][2],tms,c_avg,cmax,cmin,cms,m_avg,mmin,mmax,mms,ni_avg,no_avg,di_avg,do_avg]

    np.set_printoptions(suppress=True)
    np.savetxt("./test_data/test_tmp.csv",tmp,fmt='%.2f',delimiter=',')

#极大值归一化
def normalize_data():
    data = np.loadtxt("./test_data/test_tmp.csv", delimiter=',')
    max_x = np.loadtxt("./ML_Module/train_data/max_x.csv", delimiter=',')
    #为训练数据最大值
    for i in range(len(data)):
        if max_x[i] != 0:
            data[i] /= max_x[i]
            if(data[i]>1):
                data[i] = 1.0
        else:
            data[i] = 1.0
    np.savetxt("./test_data/test_x.csv", data,fmt='%.3f',  delimiter=',')
    
def main():
    
    #处理数据（行数）
    process_data(int(sys.argv[1]))
    #标准化数据
    normalize_data()
  
if __name__=='__main__':
    main()
 

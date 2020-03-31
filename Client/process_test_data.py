#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import numpy as np
import sys
def cal_merge_data(group_n):
    d1 = np.loadtxt("./cur_log_data/base_data.log",delimiter = ',',skiprows=1)
    d2 = np.loadtxt("./cur_log_data/load_avg.log",delimiter = ',',skiprows=1)
    
    tms = d1[0][0]-d1[0][0]
    c_avg,cmax,cmin,cms = d1[0][1],d1[0][1],d1[0][1],d1[1][1]-d1[0][1]
    m_avg,mmin,mmax,mms = d1[0][2],d1[0][2],d1[0][2],d1[1][2]-d1[1][2]
    di_avg,do_avg = d1[0][3],d1[0][4]
    ni_avg,no_avg = d1[1][5]-d1[0][5],d1[1][6]-d1[0][6]
    for j in range(1,group_n):
        if tms < d1[j][0]-d1[j-1][0]:
            tms = d1[j][0]-d1[j-1][0]
        c_avg += d1[j][1]
        if cmin > d1[j][1]:
            cmin = d1[j][1]
        if cmax < d1[j][1]:
            cmax = d1[j][1]
        if cms > d1[j][1]-d1[j-1][1]:
            cms = d1[j][1]-d1[j-1][1]
        m_avg += d1[j][2]
        if mmin > d1[j][2]:
            mmin = d1[j][2]
        if mmax < d1[j][2]:
            mmax = d1[j][2]
        if mms < d1[j][2]-d1[j-1][2]:
            mms = d1[j][2]-d1[j-1][2]
        di_avg += d1[j][3]
        do_avg += d1[j][4]
        if ni_avg < d1[j][5]-d1[j-1][5]:
            ni_avg = d1[j][5]-d1[j-1][5]
        if ni_avg < d1[j][6]-d1[j-1][6]:
            ni_avg = d1[j][6]-d1[j-1][6]
        c_avg /= group_n
        m_avg /= group_n
        di_avg /= group_n
        do_avg /= group_n
        tmp_cmax = cmax
        c_avg = 1-c_avg
        cmax = 100 - cmin
        cmin = 100 - tmp_cmax
        cms = abs(cms)
        tmp = [d2[0],d2[1],d2[2],tms,c_avg,cmin,cms,m_avg,mmin,mmax,mms,di_avg,do_avg,ni_avg,no_avg]

    np.set_printoptions(suppress=True)
    np.savetxt("./test_data/test_tmp.csv",tmp,fmt='%.2f',delimiter=',')

def normalize_data():
    data = np.loadtxt("./test_data/test_tmp.csv",delimiter=',')
    nm = np.loadtxt("./ML_Module/train_data/maxn_data.csv",delimiter=',')
    for i in range(len(data)):
        if nm[i] != 0:
            data[i] /= nm[i]
            if(data[i]>1):
                data[i] = 1.0
        else:
            data[i] = 1.0
    np.set_printoptions(suppress=True)
    #np.set_printoptions(precision=3)
    np.savetxt("./test_data/test.csv",data,fmt='%.3f',delimiter=',')
    
def main():
    cal_merge_data(20)
    normalize_data()
    print("complete!\n")
if __name__=='__main__':
    main()
 

#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import numpy as np
import sys

def cal_merge_data(group_n):
    d = np.loadtxt("./test_data/base_data.log",delimiter = ',')
    e = len(d)
    s = e - group_n
    tms = d[s+1][3]-d[s][3]
    c_avg,cmax,cmin,cms = d[s][4],d[s][4],d[s][4],d[s+1][4]-d[s][4]
    m_avg,mmin,mmax,mms = d[s][5],d[s][5],d[s][5],d[s+1][5]-d[s][5]
    di_avg,do_avg = d[s][6],d[s][7]
    ni_avg,no_avg = d[s+1][8]-d[s][8],d[s+1][9]-d[s][9]
    for j in range(s+1,e):
        if tms < d[j][3]-d[j-1][3]:
            tms = d[j][3]-d[j-1][3]
        c_avg += d[j][4]
        if cmin > d[j][4]:
            cmin = d[j][4]
        if cmax < d[j][4]:
            cmax = d[j][4]
        if cms > d[j][4]-d[j-1][4]:
            cms = d[j][4]-d[j-1][4]
        m_avg += d[j][5]
        if mmin > d[j][5]:
            mmin = d[j][5]
        if mmax < d[j][5]:
            mmax = d[j][5]
        if mms < d[j][5]-d[j-1][5]:
            mms = d[j][5]-d[j-1][5]
        di_avg += d[j][6]
        do_avg += d[j][7]
        if ni_avg < d[j][8]-d[j-1][8]:
            ni_avg = d[j][8]-d[j-1][8]
        if no_avg < d[j][9]-d[j-1][9]:
            no_avg = d[j][9]-d[j-1][9]
    c_avg /= group_n
    c_avg = 100 - c_avg
    tmp_cmax = cmax
    cmax = 100 - cmin
    cmin = 100 - tmp_cmax
    cms = abs(cms)
    m_avg /= group_n
    di_avg /= group_n
    do_avg /= group_n
    tmp = [d[e-1][0],d[e-1][1],d[e-1][2],tms,c_avg,cmax,cmin,cms,m_avg,mmin,mmax,mms,di_avg,do_avg,ni_avg,no_avg]

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
    np.savetxt("./test_data/test_x.csv",data,fmt='%.3f',delimiter=',')
    
def main():
    
    cal_merge_data(int(sys.argv[1]))
    normalize_data()
if __name__=='__main__':
    main()
 

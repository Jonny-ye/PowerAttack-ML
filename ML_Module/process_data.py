#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import numpy as np
import sys

def cal_merge_data(group_n):
    f1 = open("./log_data/base_data.log",encoding='utf-8')
    f2 = open("./log_data/load_avg.log",encoding='utf-8')
    d1 = np.loadtxt(f1,delimiter = ',',skiprows=1)
    d2 = np.loadtxt(f2,delimiter = ',',skiprows=1)
    t = int(len(d1)/group_n)
    tmp = [[0]*15]*t
    for i in range(t):
        sr = i*group_n
        tms = d1[sr+1][0]-d1[sr][0]
        cmax,cmin,cms = d1[sr][1],d1[sr][1],d1[sr+1][1]-d1[sr][1]
        m_avg,mmin,mmax,mms = d1[sr][2],d1[sr][2],d1[sr][2],d1[sr+1][2]-d1[sr][2]
        di_avg,do_avg = d1[sr][3],d1[sr][4]
        ni_avg,no_avg = d1[sr+1][5]-d1[sr][5],d1[sr+1][6]-d1[sr][6]
        for j in range(sr+1,sr+group_n):
            if tms < d1[j][0]-d1[j-1][0]:
                tms = d1[j][0]-d1[j-1][0]
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
        m_avg /= group_n
        di_avg /= group_n
        do_avg /= group_n
        tmp_cmax = cmax
        cmax = 100 - cmin
        cmin = 100 - tmp_cmax
        cms = abs(cms)
        tmp[i] = [d2[i][0],d2[i][1],d2[i][2],tms,cmax,cmin,cms,m_avg,mmin,mmax,mms,di_avg,do_avg,ni_avg,no_avg]

    np.set_printoptions(suppress=True)
    np.savetxt("./train_data/train_tmp.txt",tmp,fmt='%.2f')

def normalize_data():
    with open("./train_data/train_tmp.txt",encoding='utf-8') as f1:
        data = np.loadtxt(f1,delimiter = ' ')
        rows = len(data)
        cols = 15
        nm = [0]*15
        for j in range(cols):
            nm[j] = data[0][j]
        for i in range(1,rows):
            for j in range(cols):
                if nm[j]<data[i][j]:
                    nm[j] = data[i][j]
        for i in range(rows):
            for j in range(cols):
                if nm[j] != 0:
                    data[i][j] /= nm[j]
        np.set_printoptions(suppress=True)
        #np.set_printoptions(precision=3)
        np.savetxt("./train_data/maxn_data.txt",nm,fmt='%.3f')
        np.savetxt("./train_data/train.txt",data,fmt='%.3f')

def main():
    cal_merge_data(20)
    normalize_data()
    print("complete\n\n")
if __name__=='__main__':
    main()

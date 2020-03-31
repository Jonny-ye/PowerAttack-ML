#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import numpy as np

def cal_data(group_n):
    # 打开日志文件
    d = np.loadtxt("./log_data/base.log",delimiter = ',',skiprows=1)
    # 数据组数
    t = int(len(d)/group_n)
    tmp = []
    for i in range(t):
        s = i*group_n  #组开始行数
        e = s+group_n  #组结束行数
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
            if ni_avg < d[j][9]-d[j-1][9]:
                ni_avg = d[j][9]-d[j-1][9]
        c_avg /= group_n
        c_avg = 100 - c_avg
        tmp_cmax = cmax
        cmax = 100 - cmin
        cmin = 100 - tmp_cmax
        cms = abs(cms)
        m_avg /= group_n
        di_avg /= group_n
        do_avg /= group_n
        tmp.append([d[e-1][0],d[e-1][1],d[e-1][2],tms,c_avg,cmax,cmin,cms,m_avg,mmin,mmax,mms,di_avg,do_avg,ni_avg,no_avg])

    np.set_printoptions(suppress=True)
    np.savetxt("./train_data/train_tmp.csv",tmp,fmt='%.2f',delimiter = ',')

#采用极值归一化
def normalize_data(data_cols):
    data = np.loadtxt("./train_data/train_tmp.csv", delimiter=',')
    rows = len(data)
    cols = data_cols
    nm = [0]*cols
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
    np.savetxt("./train_data/maxn_data.csv",nm,fmt='%.3f',delimiter=',')
    np.savetxt("./train_data/train_x.csv",data,fmt='%.3f',delimiter=',')

def main():
    cal_data(20)
    normalize_data(16)
    print("complete!\n")
if __name__=='__main__':
    main()

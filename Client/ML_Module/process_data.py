#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import numpy as np

#处理数据
def process_data(group_n):
    # 打开日志文件
    d = np.loadtxt("./log_data/base.log",delimiter = ',',skiprows=1)
    # 数据组数
    t = int(len(d)/group_n)
    
    for i in range(len(d)):
        d[i][4] = 100 - d[i][4]
        d[i][6] /= 1024
        d[i][7] /= 1024
    tmp = []
    for i in range(t):
        s = i*group_n  #组开始行数
        e = s+group_n  #组结束行数
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
        tmp.append([d[e-1][0],d[e-1][1],d[e-1][2],tms,c_avg,cmin,cmax,cms,m_avg,mmin,mmax,mms,ni_avg,no_avg,di_avg,do_avg])

    np.set_printoptions(suppress=True)
    np.savetxt("./train_data/train_tmp.csv",tmp,fmt='%.2f',delimiter = ',')

#采用极值归一化
def normalize_data():
    data = np.loadtxt("./train_data/train_tmp.csv", delimiter=',')
    rows = len(data)
    cols = len(data[0])
    max_x = [0]*cols
    for i in range(rows):
        for j in range(cols):
            if max_x[j]<data[i][j]:
                max_x[j] = data[i][j]
    for i in range(rows):
        for j in range(cols):
            if max_x[j] != 0:
                data[i][j] /= max_x[j]
            else:
                data[i][j] = 1.0
    np.savetxt("./train_data/max_x.csv",max_x,fmt='%.4f',delimiter=',')
    np.savetxt("./train_data/train_x.csv",data,fmt='%.4f',delimiter=',')

def main():
    
    process_data(20)
    normalize_data()
    print("complete!\n")
    
if __name__=='__main__':
    main()

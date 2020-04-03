#!/usr/bin/python

import numpy as np

d = np.loadtxt("./train_data/train_x.csv",delimiter = ',')
rows = len(d)
cols = len(d[0])
print(rows,cols)

train_y = [] 
total = 0
for i in range(rows):
    cnt = 0;
    max = 0
    for j in range(12):
        if(d[i][j]>0.80):
            cnt += 1
    if (d[i][0]>0.8 or cnt>=4 or d[i][4]>0.8 or d[i][5]>0.8):
        train_y.append([1,0])
        total += 1
    else:
        train_y.append([0,1])
print(str(round(total/rows*100,2)) + "%")
np.savetxt("./train_data/train_y.csv", train_y, delimiter = ',',fmt="%d")

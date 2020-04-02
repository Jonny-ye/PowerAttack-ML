#!/usr/bin/pyhon

import numpy as np

d = np.loadtxt("./train_x.csv",delimiter = ',')
rows = len(d)
cols = len(d[0])

print(rows,cols)
train_y = [] 
total = 0
for i in range(rows):
    cnt = 0;
    max = 0
    for j in range(12):
        if(d[i][j]>0.8):
            cnt += 1
        if max<d[i][j]:
            max = d[i][j]
    if (d[i][0]>0.7 or cnt>=4 or max == 1.0 or d[i][4]>0.5):
        train_y.append([1,0])
        total += 1
    else:
        train_y.append([0,1])
print(str(total/rows*100) + "%")
np.set_printoptions(suppress=True)
np.savetxt("./train_y.csv", train_y, delimiter = ',',fmt="%d")

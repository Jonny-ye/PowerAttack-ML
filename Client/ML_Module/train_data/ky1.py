#!/usr/bin/python
import numpy as np

d = np.loadtxt("./train_y.csv",delimiter = ',')

cols = int(len(d)/5)

d1 = []
for i in range(cols):
    flag = 0
    for j in range(5):
        if d[i*5+j] == 1:
            flag = 1
            break
    if flag == 1:
        d1.append([1,0])
    else:
        d1.append([0,1])
np.savetxt("./train_y.csv", d1, delimiter = ',',fmt="%d")

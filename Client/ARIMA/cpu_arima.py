#!/bin/python

# -*- coding: utf-8 -*-
import os
import pandas as pd
import numpy as np
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa import arima_model
from statsmodels.stats.diagnostic import acorr_ljungbox
import warnings
warnings.filterwarnings("ignore")
import pyflux as pf
import matplotlib.pyplot as plt


def ARIMA(series,n):
    #一阶差分的ARIMA模型
    series = np.array(series)
    series = pd.Series(series.reshape(-1))
    currentDir = os.getcwd()#当前工作路径
    #一阶差分数据
    fd = series.diff(1)[1:]
    plot_acf(fd).savefig(currentDir+'/cpu一阶差分自相关图.png')
    plot_pacf(fd).savefig(currentDir+'/cpu一阶差分偏自相关图.png')
    #一阶差分单位根检验
    unitP = adfuller(fd)[1]
    if unitP>0.05:
        unitAssess = '单位根检验中p值为%.2f，大于0.05，认为该一阶差分序列判断为非平稳序列'%(unitP)
    else:
        unitAssess = '单位根检验中p值为%.2f，小于0.05，认为该一阶差分序列判断为平稳序列'%(unitP)
    #白噪声检验
    noiseP = acorr_ljungbox(fd, lags=1)[-1]
    if noiseP<=0.05:
        noiseAssess = '白噪声检验中p值为%.2f，小于0.05，认为该一阶差分序列为非白噪声'%noiseP
    else:
        noiseAssess = '白噪声检验中%.2f，大于0.05，认为该一阶差分序列为白噪声'%noiseP
    #BIC准则确定p、q值
    pMax = 3
    qMax = pMax
    bics = list()
    for p in range(pMax + 1):
        tmp = list()
        for q in range(qMax + 1):
            try:
                tmp.append(arima_model.ARIMA(series, (p, 1, q)).fit().bic)
            except Exception as e:
                #print(str(e))
                tmp.append(1e+10)#加入一个很大的数
        bics.append(tmp)
    bics = pd.DataFrame(bics)
    p, q = bics.stack().idxmin()
    print('BIC准则下确定p,q为%s,%s'%(p,q))
    model = arima_model.ARIMA(series,order=(p, 1, q))
    result = model.fit()
    predict = result.forecast(n)[0]
    return {
            'model':{'value':model,'desc':'模型'},
            'unitP':{'value':unitP,'desc':unitAssess},
            'noiseP':{'value':noiseP[0],'desc':noiseAssess},
            'p':{'value':p,'desc':'AR模型阶数'},
            'q':{'value':q,'desc':'MA模型阶数'},
            'predict':{'value':predict,'desc':'往后预测%d个的序列'%(n)}
            }

if __name__ == "__main__":
    d1 = np.loadtxt("../test_data/history.tmp", delimiter=',', usecols=4)
    e = len(d1)
    s = e-50
    res1 = ARIMA(d1[s:e],10)
    predict1 = res1['predict']['value']
    predict1 = np.round(predict1,1)
    print('CPU使用率预测值:',predict1)
    
    p = 2
    q = 2
    model_a = pf.ARIMA(d1[s:e],ar=p,ma=q,integ=0)
    x= model_a.fit()
    model_a.plot_fit()
    model_a.plot_predict(h=10,past_values=40)


#!/bin/python

# -*- coding: utf-8 -*-
import os
import time
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


def ARIMA(series,n,name):
    #一阶差分的ARIMA模型
    series = np.array(series)
    series = pd.Series(series.reshape(-1))
    currentDir = os.getcwd()#当前工作路径
    #一阶差分数据
    fd = series.diff(1)[1:]
    #plot_acf(fd).savefig('./'+ name +'一阶差分自相关图.png')
    #plot_pacf(fd).savefig('./'+ name +'一阶差分偏自相关图.png')
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
    print(result.summary())
    predict = result.forecast(n)[0]
    
    #model_a = pf.ARIMA(d1[s:e],ar=p,ma=q,integ=0)
    #x= model_a.fit()
    #model_a.plot_fit()
    #model_a.plot_predict(h=20,past_values=50)
    
    return {
            'model':{'value':model,'desc':'模型'},
            'unitP':{'value':unitP,'desc':unitAssess},
            'noiseP':{'value':noiseP[0],'desc':noiseAssess},
            'p':{'value':p,'desc':'AR模型阶数'},
            'q':{'value':q,'desc':'MA模型阶数'},
            'predict':{'value':predict,'desc':'往后预测%d个的序列'%(n)}
            }

if __name__ == "__main__":
    d1 = np.loadtxt("./ML_Module/test_data/history.tmp", delimiter=',', usecols=0)
    d2 = np.loadtxt("./ML_Module/test_data/history.tmp", delimiter=',', usecols=4)
    e = len(d1)
    s = e-40
    
    len = e-s
    x1 = np.linspace(-3*len,0,len)
    x2 = np.linspace(0,30,10)
    
    #功耗
    d1 = d1[s:e]
    res_load = ARIMA(d1,10,'load')
    pred_load = res_load['predict']['value']
    pred_load = np.round(pred_load,1)
    
    #cpu
    d2 = d2[s:e]
    res_cpu = ARIMA(d2,10,'cpu')
    pred_cpu = res_cpu['predict']['value']
    pred_cpu = np.round(pred_cpu,1)
   
    print('系统功耗预测值:',pred_load)
    print(res_load['p']['value'], res_load['q']['value'])
    print(res_load['unitP']['desc'])
    print(res_load['noiseP']['desc'])
    
    print('\nCPU使用率预测值:',pred_cpu)
    print(res_cpu['p']['value'], res_cpu['q']['value'])
    print(res_cpu['unitP']['desc'])
    print(res_cpu['noiseP']['desc'])
    
   
    plt.subplot(121)
    plt.plot(x1, d1, label='history')
    plt.plot(x2, pred_load ,color='red',linestyle='--',linewidth='1.0',label='predict')
    plt.title('Average Load Change')
    plt.xlabel('Time(s)')
    plt.ylabel('Value')
    plt.xlim(-3*len,30)
    plt.ylim(0,8)
    plt.subplot(122)
    plt.plot(x1, d2)
    plt.plot(x2, pred_cpu ,color='orange',linestyle='--',linewidth='1.0',label='predict')
    plt.title('Average CPU Usage Change')
    plt.xlabel('Time(s)')
    plt.ylabel('Value(%)')
    plt.xlim(-3*len,30)
    plt.ylim(0,100)

    plt.savefig('./ARIMA/时序预测图.png')
    plt.show()
   
   

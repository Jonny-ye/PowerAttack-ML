#!/bin/python

import sys
import time
import numpy as np

#处理数据
def process_data():
    d = np.loadtxt("./test_data/base.tmp",delimiter = ',')
    s = 0 #开始行
    e = len(d) #结束行
    
    for i in range(s,e):
        d[i][5] = round(100 - d[i][5],2)  #CPU空闲率转化为占用率
        d[i][7] = round(d[i][7]/1024,2)   #网络设备字节计数B转化为KB
        d[i][8] = round(d[i][8]/1024,2)
    
    # 保存到历史缓存文件
    col = len(d[0])
    f =  open("./test_data/history.tmp", 'a+')
    for i in range(s,e):
        for j in range(col-1):
            f.write(str(d[i][j])+',')
        f.write(str(d[i][col-1])+'\n')
    
    # 处理数据
    s_watts_avg,s_watts_max,s_watts_ms = d[s][0],d[s][0],d[s+1][0]-d[s][0]
    load15,load5,load1 = d[e-1][1],d[e-1][2],d[e-1][3]
    t_ms = d[s+1][4]-d[s][4]
    c_avg,c_max,c_ms = d[s][5],d[s][5],d[s+1][5]-d[s][5]
    m_avg,m_max,m_ms = d[s][6],d[s][6],d[s+1][6]-d[s][6]
    ni_ms,no_ms = d[s+1][7]-d[s][7],d[s+1][8]-d[s][8]
    disk_max = d[s][9]+d[s][10]
    
    for j in range(s+1,e):
            s_watts_avg+=d[j][0]
            if s_watts_max<d[j][0]:
                s_watts_max=d[j][0]
            if s_watts_ms < d[j][0]-d[j-1][0]:
                s_watts_ms = d[j][0]-d[j-1][0]
            if t_ms < d[j][4]-d[j-1][4]:
                t_ms = d[j][4]-d[j-1][4]
            c_avg += d[j][5]
            if c_max < d[j][5]:
                c_max = d[j][5]
            if c_ms < d[j][5]-d[j-1][5]:
                c_ms = d[j][5]-d[j-1][5]
            m_avg += d[j][6]
            if m_max < d[j][6]:
                m_max = d[j][6]
            if m_ms < d[j][6]-d[j-1][6]:
                mms = d[j][6]-d[j-1][6]
            if ni_ms < d[j][7]-d[j-1][7]:
                ni_ms = d[j][7]-d[j-1][7]
            if no_ms < d[j][10]-d[j-1][10]:
                no_ms = d[j][10]-d[j-1][10]
            if disk_max < d[j][9]+d[j][10]:
               disk_max = d[j][9]+d[j][10]
        
    s_watts_avg /= e
    c_avg /= e
    m_avg /= e
        
    #生成一个样本数据
    tmp = [s_watts_avg,s_watts_max,s_watts_ms,load15,load5,load1,t_ms,c_avg,c_max,c_ms,m_avg,m_max,m_ms,ni_ms,no_ms,disk_max]
    np.set_printoptions(suppress=True)
    np.savetxt("./test_data/test_tmp.csv",tmp,fmt='%.2f',delimiter=',')

#极大值归一化
def normalize_data():
    data = np.loadtxt("./test_data/test_tmp.csv", delimiter=',')
    max_x = np.loadtxt("./train_data/max_x.csv", delimiter=',')
    min_x = np.loadtxt("./train_data/min_x.csv", delimiter=',')
    num = [0]*len(max_x)
    for j in range(len(max_x)):
        num[j] = max_x[j]-min_x[j]
    for i in range(len(data)):
        if num[i] != 0:
            data[i] = (data[i]-min_x[i])/num[i]
            if(data[i]>1):
                data[i] = 1.0
        else:
            data[i] = 1.0
    # 保存测试向量    
    np.savetxt("./test_data/test_x.csv", data,fmt='%.3f',  delimiter=',')

# s型函数
def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

# s型函数偏导数
def sigmoid_derivative(x):
    return x * (1 - x)

# BP神经网络类
class BP_NeuralNetwork_Test:
    # 构建神经网络(网络每层数目，迭代次数，学习率)
    def __init__(self):
        self.inputs = []   # 输入
        self.outputs = []  # 输出
        self.layers = []   # 隐藏层
        self.weights = []  # 权重
        self.bias = []     # 偏置
        self.layer_sizes = []  # 每层隐藏层个数
        self.train_num = 0   # 训练集样本数
        self.input_num = 0   # 样本总数
        self.layer_num = 0  # 神经网络层数（不计输入层）
        
    # 正向传播
    def forward_propagate(self, _input):
        self.layers = []
        self.layers.append(_input)
        for i in range(self.layer_num):
            raw_val = np.dot(self.layers[i], self.weights[i]) + self.bias[i]
            val = sigmoid(raw_val)
            #print(val)
            self.layers.append(val)
    
    # 测试模型(离线模式)
    def test(self):
        #加载保存的模型
        self.inputs = np.loadtxt("./test_data/test_x.csv", delimiter=',')
        self.layer_sizes = np.loadtxt("./model/layer_sizes.mat")
        self.layer_num = len(self.layer_sizes) - 1
        for i in range(self.layer_num):
            file_weights = "./model/weights" + str(i) + ".mat"
            self.weights.append(np.loadtxt(file_weights))
            file_bias = "./model/bias" + str(i) + ".mat"
            self.bias.append(np.loadtxt(file_bias))
        
        #进行一次正向传播
        self.forward_propagate(self.inputs)
        if(self.layers[self.layer_num][0]>0.5):
            print("[警告]可能有潜在电力攻击 ")
        else:
            print("[安全]无电力攻击风险 ")
        #加载关键数据
        d = np.loadtxt("./test_data/test_tmp.csv")
        net = d[12]
        if(net < d[13]):
            net = d[13]
        net /= 1024
        
        #平均功耗，CPU平均占用，CPU峰值，内存平均使用，网络峰值
        print(d[0],d[7],d[8],d[9],round(net,3)) 
        
        
def main():
    
    # 预处理数据
    process_data()
    # 归一化数据
    normalize_data()
    # 构建BP神经网络
    bp = BP_NeuralNetwork_Test()
    # 检测数据
    bp.test()
   
if __name__ == "__main__":
    main()
 

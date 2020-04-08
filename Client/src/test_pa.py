#!/bin/python

import sys
import time
import numpy as np

#处理数据
def process_data():
    d = np.loadtxt("./test_data/base.tmp",delimiter = ',')
    s = 0
    e = len(d)
    
    for i in range(s,e):
        d[i][4] = 100 - d[i][4]
        d[i][6] /= 1024
        d[i][7] /= 1024
    
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
        
    c_avg /= e
    m_avg /= e
    di_avg /= e
    do_avg /= e
    tmp = [d[e-1][0],d[e-1][1],d[e-1][2],tms,c_avg,cmax,cmin,cms,m_avg,mmin,mmax,mms,ni_avg,no_avg,di_avg,do_avg]

    np.set_printoptions(suppress=True)
    np.savetxt("./test_data/test_tmp.csv",tmp,fmt='%.2f',delimiter=',')

#极大值归一化
def normalize_data():
    data = np.loadtxt("./test_data/test_tmp.csv", delimiter=',')
    max_x = np.loadtxt("./ML_Module/train_data/max_x.csv", delimiter=',')
    #为训练数据最大值
    for i in range(len(data)):
        if max_x[i] != 0:
            data[i] /= max_x[i]
            if(data[i]>1):
                data[i] = 1.0
        else:
            data[i] = 1.0
    np.savetxt("./test_data/test_x.csv", data,fmt='%.3f',  delimiter=',')

#保存历史
def save_history():
    d = np.loadtxt("./test_data/base.tmp",delimiter = ',')
    row = len(d)
    col = len(d[0])
    localtime = time.asctime( time.localtime(time.time()) )
    file = r'test.txt'
    f =  open("./test_data/history.tmp", 'a+')
    f.write(localtime+'\n')
    for i in range(row):
        for j in range(col-1):
            f.write(str(d[i][j])+',')
        f.write(str(d[i][col-1])+'\n')
    

# s型函数
def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

# s型函数偏导数
def sigmoid_derivative(x):
    return x * (1 - x)

# BP神经网络类
class BP_NeuralNetwork:
    # 构建神经网络(网络每层数目，迭代次数，学习率)
    def __init__(self, layer_sizes, _limit, learn_rate):
        self.inputs = []   # 输入
        self.outputs = []  # 输出
        self.layers = []   # 隐藏层
        self.weights = []  # 权重
        self.bias = []     # 偏置
        self.layer_sizes = layer_sizes  # 每层隐藏层个数
        
        self.train_num = 0   # 训练集样本数
        self.input_num = 0   # 样本总数
        self.layer_num = len(layer_sizes) - 1  # 神经网络层数（不计输入层）
        self.learn_rate = learn_rate   # 学习率
        self._limit = _limit           # 迭代次数
        self._train = 0.8              # 80%样本作为训练集，20%样本作为验证集
        self._accuracy = 0.001         # 学习精度
    
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
        #加载数据和保存的模型
        self.inputs = np.loadtxt("./test_data/test_x.csv", delimiter=',')
        self.layer_sizes = np.loadtxt("./ML_Module/model/layer_sizes.mat")
        self.layer_num = len(self.layer_sizes) - 1
        for i in range(self.layer_num):
            file_weights = "./ML_Module/model/weights" + str(i) + ".mat"
            self.weights.append(np.loadtxt(file_weights))
            file_bias = "./ML_Module/model/bias" + str(i) + ".mat"
            self.bias.append(np.loadtxt(file_bias))
        
        self.forward_propagate(self.inputs)
        if(self.layers[self.layer_num][0]>0.5):
            print("[警告]可能有潜在电力攻击 ")
        else:
            print("[安全]_无电力攻击风险 ")

        #info = "平均负载：" \+ str(d[0]) + "  cpu_avg:" + str(d[4]) + "%  cpu_max:" + str(d[5]) + "%  mem_avg:" + str(d[8])+ "MB\n" 
        #print(info)
        d = np.loadtxt("./test_data/test_tmp.csv")
        net = d[12]
        if(net < d[13]):
            net = d[13]
        net /= 1024
        print(d[0],d[4],d[5],d[8],round(net,3))
        
        
def main():
    
    process_data()
    
    normalize_data()
    
    save_history()
    
    # 构建BP神经网络
    bp = BP_NeuralNetwork([16,12,6,2], 5000, 0.3)
    # 离线测试
    bp.test()
   
if __name__ == "__main__":
    main()
 

#!/bin/python

import sys
import datetime
import numpy as np

# s型函数
def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

# s型函数偏导数
def sigmoid_derivative(x):
    return x * (1 - x)

# 计算时间
def show_time_used(st, et):
    print("训练完成，用时：" + str((et - st).seconds) + 's')

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
        
        print("本地机器学习模型计算结果：")
        self.forward_propagate(self.inputs)
        if(self.layers[self.layer_num][0]>0.5):
            print("[警告] 服务器可能存在潜在的电力攻击！")
            d = np.loadtxt("./test_data/test_tmp.csv")
            info = "平均负载：" + str(d[0]) + "  cpu_avg:" + str(d[4]) + "%  cpu_max:" + str(d[5]) + "%  mem_avg:" + str(d[8])+ "MB\n" 
            print(info)
        else:
            print("[安全] 服务器暂无电力攻击风险。\n")
        
def main():
    
    # 构建BP神经网络
    bp = BP_NeuralNetwork([16,12,6,2], 5000, 0.3)
    # 离线测试
    bp.test()

if __name__ == "__main__":
    main()
 

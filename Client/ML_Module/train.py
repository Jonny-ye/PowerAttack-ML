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
            
    # 初始化训练数据
    def init_data(self):
        # 初始化输入输出
        self.inputs = np.loadtxt("./train_data/train_x.csv", delimiter=',')
        self.outputs = np.loadtxt("./train_data/train_y.csv", delimiter=',')
        self.input_num = len(self.inputs)
        print("样本总数：" + str(self.input_num))
        self.train_num = int(self.input_num*self._train)
        # 初始化权重和偏置
        for i in range(self.layer_num):
            self.weights.append(np.random.rand(self.layer_sizes[i], self.layer_sizes[i + 1]))
            self.bias.append(np.random.rand(1, self.layer_sizes[i + 1]))
        
    # 正向传播
    def forward_propagate(self, _input):
        self.layers = []
        self.layers.append(_input)
        for i in range(self.layer_num):
            raw_val = np.dot(self.layers[i], self.weights[i]) + self.bias[i]
            val = sigmoid(raw_val)
            self.layers.append(val)
    
    # 反向传播
    def back_propagate(self, _output):
        theta = []
        theta_output = (self.layers[-1] - _output) * sigmoid_derivative(self.layers[-1])
        theta.append(theta_output)
        for i in range(self.layer_num - 1, 0, -1):
            theta_layer = np.dot(theta[-1], self.weights[i].T) * sigmoid_derivative(self.layers[i])
            theta.append(theta_layer)
        theta.reverse()
        for i in range(self.layer_num):
            la = self.layers[i].reshape(self.layer_sizes[i], 1)
            self.weights[i] -= np.multiply(la, theta[i]) * self.learn_rate
            self.bias[i] -= theta[i] * self.learn_rate

        return sum((self.layers[-1] - _output) ** 2 / 2)

    # 训练模型
    def train(self):
        for i in range(self._limit): 
            # 使用部分进行训练
            for j in range(self.train_num):
                self.forward_propagate(self.inputs[j])
                if self.back_propagate(self.outputs[j]).any() < self._accuracy:
                    return
    
    # 验证模型
    def validate(self):
        predict_y = []
        for i in range(self.train_num,self.input_num):
            self.forward_propagate(self.inputs[i])
            predict_y.append(self.layers[self.layer_num])
        np.set_printoptions(suppress=True)
        #np.savetxt("./train_data/predict_real.txt", predict_y, fmt='%.3f')
        rows = len(predict_y)
        cols = len(predict_y[0][0])
        for i in range(rows):
            for j in range(cols):
                if predict_y[i][0][j] > 0.5:
                    predict_y[i][0][j] = 1
                else:
                    predict_y[i][0][j] = 0
        cnt = rows
        print("验证集测试结果:")
        for i in range(rows):
            print(predict_y[i])
            for j in range(cols):
                if predict_y[i][0][j] != self.outputs[i+self.train_num][j]:
                    cnt -= 1
                    break
        print("验证集预测准确度：" + str(cnt / len(predict_y) * 100) + "%")
    
    # 测试模型(离线模式)
    def test(self):
        #加载数据和保存的模型
        self.inputs = np.loadtxt("./test_data/test_x.csv", delimiter=',')
        self.layer_sizes = np.loadtxt("./model/layer_sizes.mat")
        self.layer_num = len(self.layer_sizes) - 1
        for i in range(self.layer_num):
            file_weights = "./model/weights" + str(i) + ".mat"
            self.weights.append(np.loadtxt(file_weights))
            file_bias = "./model/bias" + str(i) + ".mat"
            self.bias.append(np.loadtxt(file_bias))
        #正向传播计算
        predict_y = []
        for i in range(len(self.inputs)):
            self.forward_propagate(self.input[i])
            predict_y.append(self.layers[self.layer_num])
        
        print(predict_y)
 
    # 保存模型
    def save_model(self):
        np.savetxt("./model/layer_sizes.mat", self.layer_sizes)
        for i in range(self.layer_num):
            file_weights = "./model/weights" + str(i) + ".mat"
            np.savetxt(file_weights, self.weights[i])
            file_bias = "./model/bias" + str(i) + ".mat"
            np.savetxt(file_bias, self.bias[i])

    
def main():
    
    ## 构建BP神经网络
    bp = BP_NeuralNetwork([16,12,6,2], 10000, 0.4)
    
    # 加载训练数据  (网络每层数目，迭代次数, 学习率，学习精度，训练样本比例)
    bp.init_data()    
    
    # 训练模型
    start_time = datetime.datetime.now()
    bp.train()
    end_time = datetime.datetime.now()
    show_time_used(start_time, end_time)
    
    # 验证模型
    bp.validate()
    
    # 保存模型
    bp.save_model()


if __name__ == "__main__":
    main()
 

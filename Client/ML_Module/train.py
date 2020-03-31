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
    print("BP神经网络训练用时：" + str((et - st).seconds) + 's')

# BP神经网络类
class BP_NeuralNetwork:
    def __init__(self):
        self.inputs = []  # 输入
        self.outputs = []  # 输出
        self.trian_num = 0   # 训练样本数
        self.input_num = 0   # 样本数
        self.layers = []  # 隐藏层
        self.layer_sizes = []  # 每层隐藏层个数
        self.layer_num = 0  # 神经网络层数
        self.weights = []  # 权重
        self.bias = []  # 偏置
        self.learn_rate = 0  # 学习率
        self.limit = 0  # 迭代次数
        self.accuracy = 0.001  # 学习精度
            
    # 加载训练数据(网络每层数目，学习率，迭代次数，学习精度，训练样本比例)
    def init_data(self, layer_sizes, _limit, learn_rate, _accuracy，_train):
        self.inputs = np.loadtxt("./train_data/train_x.csv", delimiter=',')
        self.outputs = np.loadtxt("./train_data/train_y.csv", delimiter=',')
        self.input_num = len(self.inputs)
        self.train_num = int(self.input_num*0.8)
        self.layer_sizes = layer_sizes
        self.layer_num = len(layer_sizes) - 1
        for i in range(self.layer_num):
            self.weights.append(np.random.rand(self.layer_sizes[i], self.layer_sizes[i + 1]))
            self.bias.append(np.random.rand(1, self.layer_sizes[i + 1]))
        self.learn_rate = learn_rate
        self.limit = _limit
        self.accuracy = _accuracy
    
    # 前向传播
    def forward_propagate(self, _input):
        self.layers = []
        self.layers.append(_input)
        for i in range(self.layer_num):
            raw_val = np.dot(self.layers[i], self.weights[i]) + self.bias[i]
            val = sigmoid(raw_val)
            self.layers.append(val)
    
    # 后向传播
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
        for i in range(self.train_num): # 使用数据部分进行训练
            for j in range(_sizes)
                self.forward_propagate(self.inputs[j])
                if self.back_propagate(self.outputs[j]).any() < self.accuracy:
                    return
    
    # 验证模型
    def validate(self):
        for i in range(self.train_num,self.input_num):
            self.forward_propagate(self.input[i])
            predict_y.append(self.layers[self.layer_num])
        np.set_printoptions(suppress=True)
        #np.savetxt("./train_data/predict_real.txt", predict_y, fmt='%.3f')
        
        rows = len(predict_y)
        cols = len(predict_y[0])
        for i in range(rows):
            for j in range(cols):
                if predict_y[i][j] > 0.5:
                    predict_y[i][j] = 1
                else:
                    predict_y[i][j] = 0
        # print(predict_y)
        cnt = rows
        for i in range(rows):
            for j in range(cols):
                if predict_y[i][j] != self.output[i+self.train_num][j]:
                    cnt -= 1
                    break
        print("验证集预测准确度：" + str(cnt / len(predict_y) * 100) + "%")

    # 保存模型
    def save_model(self):
        np.savetxt("./model/layer_sizes.mat", self.layer_sizes)
        for i in range(self.layer_num):
            file_weights = "./model/weights" + str(i) + ".mat"
            np.savetxt(file_weights, self.weights[i])
            file_bias = "./model/bias" + str(i) + ".mat"
            np.savetxt(file_bias, self.bias[i])

    
def main():
    
    # 构建BP神经网络
    bp = BP_NeuralNetwork()
    
    # 加载训练数据  (网络每层数目，迭代次数, 学习率，学习精度，训练样本比例)
    bp.init_train([16, 8, 8, 2], int(sys.argv[1]), 0.4, 0.01, 0.8)    
    
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

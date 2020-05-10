#!/bin/python

import sys
import datetime
import numpy as np
import matplotlib.pyplot as plt

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
        self._train = 0.7              # 80%样本作为训练集，20%样本作为验证集
        self._accuracy = 0.001         # 学习精度
        self.flag = 0
        self.train_rate = []
        self.test_rate = []
        self.test_pa_rate = []
        self.nset = []
            
    # 初始化训练数据
    def init_data(self):
        # 初始化输入输出
        self.inputs = np.loadtxt("./train_data/train_x.csv", delimiter=',')
        self.outputs = np.loadtxt("./train_data/train_y.csv", delimiter=',')
        self.input_num = len(self.inputs)
        print("样本总数：" + str(self.input_num) + "，迭代次数：" +str(self._limit) + "，学习率：" + str(self.learn_rate) )
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

   
    def validate_train_set(self):
        predict_y = []
        for i in range(self.train_num):
            self.forward_propagate(self.inputs[i])
            predict_y.append(self.layers[self.layer_num])
        
        #保存原始结果
        #np.set_printoptions(suppress=True)
        #np.savetxt("./train_data/predict_real.txt", predict_y, fmt='%.3f')
        
        rows = len(predict_y)
        cols = len(predict_y[0][0])
        for i in range(rows):
            for j in range(cols):
                if predict_y[i][0][j] > 0.5:
                    predict_y[i][0][j] = 1
                else:
                    predict_y[i][0][j] = 0
        cnt = 0
        cntpa = 0
        cntpa_pre = 0
        for i in range(rows):
            if self.outputs[i][0]==1:
                if predict_y[i][0][0] == 1:
                    cntpa_pre += 1
                cntpa += 1
            if predict_y[i][0][0] == self.outputs[i][0]:
                cnt += 1
        #print("训练集测试结果:")
        #print("训练集预测准确度：" + res + "%")
        #print("电力攻击识别准确度：" + str(round(100.0*cntpa_pre/cntpa,2)) + "%",cntpa_pre,cntpa)
        res = str(round(100.0*cnt/rows,2))
        return res
    # 验证模型
    def validate(self):
        predict_y = []
        for i in range(self.train_num,self.input_num):
            self.forward_propagate(self.inputs[i])
            predict_y.append(self.layers[self.layer_num])
        
        #保存原始结果
        #np.set_printoptions(suppress=True)
        #np.savetxt("./train_data/predict_real.txt", predict_y, fmt='%.3f')
        
        rows = len(predict_y)
        cols = len(predict_y[0][0])
        for i in range(rows):
            for j in range(cols):
                if predict_y[i][0][j] > 0.5:
                    predict_y[i][0][j] = 1
                else:
                    predict_y[i][0][j] = 0
        #np.set_printoptions(suppress=True)
        #np.savetxt("./train_data/predict_real.txt", predict_y, fmt='%.3f')

        cnt = 0
        cntpa = 0
        cntpa_pre = 0
        cntpa_pre_all = 0
        for i in range(rows):
            if self.outputs[i+self.train_num][0]==1:
                if predict_y[i][0][0] == 1:
                    cntpa_pre += 1
                cntpa += 1
            if predict_y[i][0][0] == 1:
                cntpa_pre_all += 1
            if predict_y[i][0][0] == self.outputs[i+self.train_num][0]:
                cnt += 1
        if cntpa_pre_all>35:
            print(cntpa_pre/cntpa_pre_all,cntpa_pre/cntpa,cntpa_pre*2/(cntpa_pre_all+cntpa))
        #print("验证集测试结果:")
        res = str(round(100.0*cnt/rows,2))
        #print("验证集预测准确度：" + res + "%")
        res_pa = str(round(100.0*cntpa_pre/cntpa,2))
        train_res = self.validate_train_set()
        self.train_rate.append(float(train_res))
        self.test_rate.append(float(res))
        self.test_pa_rate.append(float(res_pa))
        #print("电力攻击识别准确度：" + res + "%",cntpa_pre,cntpa)
        return float(res_pa)
        
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
        d1 = self.train_rate
        d2 = self.test_rate
        d3 = self.test_pa_rate
        x = self.nset
        #print(d1,d2,d3,x)
        
        plt.subplot(121)
        plt.plot(x, d1, label='training set')
        plt.plot(x, d2, label='validation set')
        plt.title('Verification Set Accuracy (Learning Rate=0.1)')
        plt.xlabel('Number of Iterations')
        plt.ylabel('Rate(%)')
        plt.xlim(self.flag-50,1000)
        plt.ylim(50,100)
        plt.legend(['validation set','training set'],loc='lower right')
        plt.subplot(122)
        plt.plot(x, d3)
        plt.title('Accuracy of Power Attack Identification')
        plt.xlabel('Number of Iterations')
        plt.ylabel('Rate(%)')
        plt.ylim(0,100)
        plt.xlim(self.flag-10,self.flag+30)
        plt.show()
    # 训练模型
    def train(self):
        for i in range(self._limit): 
            # 使用部分进行训练
            if i%100==0:
                print("完成：",i,self.learn_rate)
            if i > 300:
                k = self.validate()
                if self.flag==0 and k > 0:
                    self.flag = i+1
                self.nset.append(i)
            for j in range(self.train_num):
                # 正向传播计算结果
                self.forward_propagate(self.inputs[j])
                # 反向传播计算偏差及权重偏置修正
                if self.back_propagate(self.outputs[j]).any() < self._accuracy:
                    return
def main():
    
    ## 构建BP神经网络(网络每层数目，迭代次数, 学习率)
    bp = BP_NeuralNetwork([16,16,8,2], 1000, 0.1)
    # 加载训练数据  
    bp.init_data()    
    # 训练模型
    start_time = datetime.datetime.now()
    bp.train()
    end_time = datetime.datetime.now()
    show_time_used(start_time, end_time)
    # 验证模型
    #bp.validate()
    # 保存模型
    bp.save_model()

if __name__ == "__main__":
    main()
 

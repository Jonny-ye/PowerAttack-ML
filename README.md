## 基于机器学习的数据中心电力攻击检测系统
### /Client: 客户端

1.其中 ML_Module 文件夹为机器学习模型模块，通过模拟不同类型电力攻击的方式生成日志信息，经过数据预处理（特征工程）生成机器学习数据，训练BP神经网络，以达到最佳的潜在电力攻击的识别效果;

2.向服务器发送定时请求，将服务器的实时数据进行预处理，输入保存的BP神经网络，根据出处结果判断当前服务器是否有潜在的电力攻击风险

3.对可能存在电力攻击的情况，输出测试数据中的几项关键信息，供运维人员参考


### /Server 服务器

1.运行在监控的服务器端，启动后自动开启日志数据采集子进程，并等待客户端连接。

2.对客户端的定时请求，将特定时长日志数据发送给客户端。

3.采用java Socket多线程技术，支持多个客户端连接。


#### 开发语言：Java、Python、Bash Script
#### 运行环境：服务器：Centos，客户端：各Linux发行版

1.程序说明
(1)搜集数据：collect_log.sh

$ ./collect_log.sh 10800 
（设置采集时间）

(2)处理数据：process_data.py

$ ./process_data.py

(3)训练BP神经网络模型：train.py

$ ./train_pa.py
(在程序中设置：网络结构、迭代次数、学习率等)

2.文件夹说明
(1)train_data:训练数据
（开始训练前，将样本数据对应的train_y.csv(是否有电力攻击行为)从外部导入）

(2)model:保存的模型

(3)data:原始数据

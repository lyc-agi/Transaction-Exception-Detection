# transaction-exception-detection
通过聚类分析交易流水检测异常交易

聚类模块（transaction_cluster.py）先将正常的交易流水（正样本）聚类，计算聚类中心（保存在centers1.csv）和每个聚类中的数据离聚类中心的最大距离。然后通过正、黑样本组成的训练集对模型进行训练找到最佳阈值（保存在thresholds1.csv）。测试模块（transac_exception_detect.py）计算未知样本和各聚类中心的欧式距离，如果小于任何一个聚类中心对应的阈值，则判断为正样本，反之，只有大于所有聚类中心对应的阈值才认为是黑样本。最后输出准确率，并将黑样本的编号保存为class_result.csv文件。

提示：  
聚类模块已经运行过（即centers1.csv和thresholds1.csv均有效），可以直接运行测试模块。   
  
2020年7月17日  
2021年6月30日更新

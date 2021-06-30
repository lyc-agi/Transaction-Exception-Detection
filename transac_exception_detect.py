import sys, os
import math
import csv

def distance(v1, v2):#计算距离
    if len(v1) != len(v2):#两个数据的维数不一致
        print(sys.stderr, "invalid v1 and v2 !")
        sys.exit(1)
    distance = 0#距离值的初始化
    for i in range(len(v1)):
        distance += (v1[i] - v2[i]) ** 2
    distance = math.sqrt(distance)#欧式距离
    return distance

def classification(testdata, testbdata,centers,thresholds):#根据数据离聚类中心的距离判断是否为异常交易
    class_black_list=[]#分类为黑样本的测试集编号的列表初始化
    class_black_num=0#分类为黑样本的数量值初始化
    class_right_num=0#分类为黑样本的数量值初始化
    for i in range(len(testdata)):#依次取正样本测试数据
        for j in range(len(centers)):#依次取各个聚类中心
            dist=distance(testdata[i],centers[j])#计算距离
            if dist<thresholds[j]:#比任一聚类中的阈值小就认为是正样本
                class_right_num+=1#正样本计数加一
                break#不用看其他聚类了，跳出内层循环，直接取下一个测试数据
            if dist>=thresholds[j] and j==len(centers)-1:#如果聚类中心都比较完了仍然大于阈值，认为是黑样本
                class_black_list.append(i)#保存测试样本的编号
    for i in range(len(testbdata)):#依次取黑样本测试数据
        for j in range(len(centers)):#依次取各个聚类中心
            dist=distance(testbdata[i],centers[j])#计算距离
            if dist<thresholds[j]:#比任一聚类中的阈值小就认为是正样本，判断错误
                break#不用看其他聚类了，跳出内层循环，直接取下一个测试数据
            if dist>=thresholds[j] and j==len(centers)-1:#如果聚类中心都比较完了仍然大于阈值，认为是黑样本，判断正确
                class_black_num+=1
                class_black_list.append(i+len(testdata))#但是仍然保存测试样本的编号

    #class_black_num=1000#测试用
    print("黑样本判断准确率：")
    print(class_black_num/len(testbdata))#黑样本分类准确率，注：python3后，整型数字的除法运算也默认使用浮点数运算，所以不用转化为浮点型
    print("正样本判断准确率：")
    print(class_right_num/len(testdata))#正样本分类准确率
    print("分类准确率：")
    print((class_black_num+class_right_num)/(len(testbdata)+len(testdata)))#总分类准确率
    return class_black_list

if __name__ == '__main__':
    #with open("E:\\dm\\trainingdata.csv", "r",encoding="utf-8") as f:#取总数据集中的随机正样本数据作为测试集
    with open("datasets\\500right.csv", "r",encoding="utf-8") as f:#读取正样本测试文件
            reader = csv.reader(f)
            testdata=list(reader)#样本数据转化为列表格式
            testdatafinal=[]#最终用于测试的数据
            #print("项名称及数据前10项：")
            #print(testdata[0:10])
            for list_num in range(len(testdata)):
            #for list_num in range(1300,60300,500):#读取随机产生的数据集作为测试集
                testdata[list_num]=[ float(x) for x in testdata[list_num]]#数据从字符串转化为浮点，便于之后的计算             
                testdatafinal.append(testdata[list_num]) #生成加工后的最终的测试数据
    with open("datasets\\500black.csv", "r",encoding="utf-8") as f:#读取黑样本测试文件
            reader = csv.reader(f)
            testbdata=list(reader)#样本数据转化为列表格式
            testbdatafinal=[]#最终用于测试的数据
            #print("项名称及数据前10项：")
            #print(testdata[0:10])
            for list_num in range(len(testbdata)):
                testbdata[list_num]=[ float(x) for x in testbdata[list_num]]#数据从字符串转化为浮点，便于之后的计算             
                testbdatafinal.append(testbdata[list_num]) #生成加工后的最终的测试数据

    with open("datasets\\centers1.csv", "r",encoding="utf-8") as f:#读取聚类中心文件
            reader = csv.reader(f)
            centers=list(reader)#转化为列表格式
            for list_num in range(len(centers)):
                centers[list_num]=[float(x) for x in centers[list_num]]#转化为浮点型
            print("提示：聚类中心已读入")
            #print("聚类中心：")
            #print(centers)

    with open("datasets\\thresholds1.csv", "r",encoding="utf-8") as f:#读取阈值文件
            reader = csv.reader(f)
            data=list(reader)#转化为列表格式
            thresh=[float(x) for x in data[0]]#转化为浮点型，同时转化为一维列表
            #thresh=[x*0.9 for x in thresh]#测试用
            print("提示：判定阈值已读入")
            #print("阈值：")
            #print(thresh)

    class_result=classification(testdatafinal,testbdatafinal,centers,thresh)#分类

    print("模型判断的黑样本的编号：")
    print(class_result)

    with open("class_result.csv", "w",newline= '') as csvFile:     # 输出分类结果（黑样本的编号）
           csvWriter = csv.writer(csvFile)
           csvWriter.writerow(class_result)



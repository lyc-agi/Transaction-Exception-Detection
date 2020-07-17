import sys, os
import math
import csv

class Hierarchical:#凝聚型层次聚类的类
    def __init__(self, center, left = None, right = None, flag = None, distance = 0.0):
        self.center = center#聚类中心
        self.left = left#合并数据的编号之一
        self.right = right#合并数据的编号之二
        self.flag = flag#标签，记录是否被处理过
        self.distance = distance

def traverse(node):#合并类
    if node.left == None and node.right == None:#没有合并过的类，即初始数据，递归出口
        return [node.center]
    else:
        return traverse(node.left) + traverse(node.right)#合并过的数据聚在一类

def distance(v1, v2):#计算距离
    if len(v1) != len(v2):#两个数据的维数不一致
        print(sys.stderr, "invalid v1 and v2 !")
        sys.exit(1)
    distance = 0#距离值的初始化
    for i in range(len(v1)):
        distance += (v1[i] - v2[i]) ** 2
    distance = math.sqrt(distance)#欧式距离
    return distance

def hcluster(data, n):#聚类过程
    if len(data) <= 0:#无数据则退出
        print(sys.stderr, "invalid data")
        sys.exit(1)
    clusters = [Hierarchical(data[i], flag = i) for i in range(len(data))]#初始化，每条数据都是一个类
    centers = [data[i] for i in range(len(data))]#聚类中心初始化为每条数据，之后的操作与聚类操作保持同步
    distances = {}#存储距离的字典初始化
    min_id1 = None#两个最接近的数据编号之1
    min_id2 = None#两个最接近的数据编号之2
    currentCluster = -100#作为flag的值，记录当前形成的聚类
    while(len(clusters) > n):#聚类结束条件：聚成小于n个类
        minDist = 1000000000000#最小距离初始化，初始值设置为非常大的值，因为相接近的数据的距离也可能很大，以此避免误判
        for i in range(len(clusters) - 1):
            for j in range(i + 1, len(clusters)):
                if distances.get((clusters[i].flag, clusters[j].flag)) == None:#如果之前没有计算过两条数据的距离
                    distances[(clusters[i].flag, clusters[j].flag)] = distance(clusters[i].center, clusters[j].center)#计算距离并存入字典
                if distances[(clusters[i].flag, clusters[j].flag)] <= minDist:#距离小于或等于之前的最小距离，则更新两条数据的类的编号及距离
                    min_id1 = i
                    min_id2 = j
                    minDist = distances[(clusters[i].flag, clusters[j].flag)]
        if min_id1 != None and min_id2 != None and minDist != 1000000000000:#如果距离更新了则更新聚类中心
            newCenter = [(clusters[min_id1].center[i] + clusters[min_id2].center[i])/2 for i in range(len(clusters[min_id2].center))] 
            newFlag = currentCluster
            currentCluster -= 1#改变下一个flag的值
            newCluster = Hierarchical(newCenter, clusters[min_id1], clusters[min_id2], newFlag, minDist)
            del clusters[min_id2]#删除这两条已经聚类的数据
            del clusters[min_id1]
            del centers[min_id2]#删除这两条已经聚类的数据的聚类中心
            del centers[min_id1]
            clusters.append(newCluster)#增加这两条数据聚类后的类
            centers.append(newCenter)#增加这两条数据聚类后的聚类中心，与对应的类保持对应
    finalCluster = [traverse(clusters[i]) for i in range(len(clusters))]#生成聚类结果
    finalCenters = centers#生成对应的聚类中心
    return finalCluster, finalCenters

def maxdists(cluster, centers):#计算各类中所有数据离聚类中心的距离和最大距离
    if len(cluster) != len(centers):#聚类的数量和聚类中心的数量不一致，提示并退出
        print(sys.stderr, "错误：聚类的数量和聚类中心的数量不一致!")
        sys.exit(1)
    max_dist_list=[]#最大距离列表初始化，各最大距离顺序与聚类中心列表对应
    dists_list=[]#每个数据离聚类中心的距离的列表初始化，用于之后确定阈值
    for i in range(len(cluster)):#依次取各个聚类      
        dists_icluster=[]#保存每个数据离聚类中心的距离，每个聚类开始时初始化一次  
        for j in range(len(cluster[i])):#计算各个聚类的各个数据离聚类中心的距离
            dist = 0#距离值的初始化
            max_dist=0#最大距离值的初始化
            for k in range(len(cluster[i][j])):#计算各个聚类的各个数据离聚类中心的距离
                dist += (cluster[i][j][k] - centers[i][k]) ** 2
            dist = math.sqrt(dist)
            dists_icluster.append(dist)#保存该数据离聚类中心的距离
            if dist>max_dist:#比较是否比目前的最大值大
                max_dist=dist       
        dists_list.append(dists_icluster)#第i个聚类的每个数据离聚类中心的距离的列表加入总距离列表
        max_dist_list.append(max_dist)#保存最终的最大距离
    return max_dist_list,dists_list

def besthres(blackdata,rightdists,maxdists,centers):#确定最佳阈值
    thresholds=[]#保存最佳阈值的列表，顺序与聚类中心列表对应
    black_dists=[None]*len(centers)#黑样本距离列表初始化，将黑样本的距离根据最近的聚类中心划分，顺序与聚类中心列表对应
    for i in range(len(centers)):
        thresholds.append(-1)#将阈值列表初始化
    for i in range(len(blackdata)):#黑样本找到最接近的聚类中心       
        min_dist=1000000000000#最小距离值的初始化
        for j in range(len(centers)):#计算黑样本离各个聚类中心的距离
            dist=distance(blackdata[i],centers[j])                    
            if dist<min_dist:#比较是否比目前最小距离小
                min_dist=dist
                closest_center=j
        if  black_dists[closest_center]==None:#之前没有黑样本最接近该聚类中心，创建列表
            black_dists[closest_center]=[]
            black_dists[closest_center].append(min_dist)#加入最近距离
        else:
            black_dists[closest_center].append(min_dist)#直接加入最近距离

    for i in range(len(centers)):#为每个聚类确定阈值
            if black_dists[i]==None:#没有黑样本最接近该聚类中心
                thresholds[i]=maxdists[i]#直接用正样本离聚类中心的最大距离作为阈值               
            else:
                weight=1.0#最大距离的权重
                min_error_num=100000#最小错误数量
                thres=maxdists[i]#初始阈值                
                for j in range(401):
                    blackin_num=0#黑样本当成正样本的数量
                    rightout_num=0                  
                    for bd in black_dists[i]:
                        if bd<=thres:#在边界上也被认为是正样本
                            blackin_num+=1
                    for rd in rightdists[i]:
                        if rd>thres:
                            rightout_num+=1
                    error_num=blackin_num*2+rightout_num#错误数量（黑样本当成正样本的数量加权，因为黑样本比较少，而且找出异常交易比将正常交易当成异常更加重要）
                    if error_num<min_error_num:#找到最小错误数量
                        min_error_num=error_num
                        besthreshold=thres
                    weight-=0.001#权重从1到0.6变化，找到最佳权重
                    thres=maxdists[i]*weight
                thresholds[i]=besthreshold   
                
    return thresholds


if __name__ == '__main__':
    with open("E:\\dm\\trainingdata1.csv", "r",encoding="utf-8") as f:#读入正样本聚类数据集
        reader = csv.reader(f)
        traindata=list(reader)#样本数据转化为列表格式
        traindatafinal=[]#最终用于训练的数据
        #print("项名称及数据前10项：")
        #print(traindata[0:10])
        for list_num in range(0,100000,100):#10万条数据随机选择1000条
            traindata[list_num]=[ float(x) for x in traindata[list_num]]#数据从字符串转化为浮点，便于之后的计算
            traindatafinal.append(traindata[list_num]) #生成加工后的最终的训练数据

    with open("E:\\dm\\blackdata1.csv", "r",encoding="utf-8") as f:#读入黑样本训练数据集
        reader = csv.reader(f)
        blackdata=list(reader)#样本数据转化为列表格式
        blackdatafinal=[]#最终用于训练的数据
        #print("黑样本项名称及数据前10项：")
        #print(blackdata[0:10])
        for list_num in range(len(blackdata)):
            blackdata[list_num]=[ float(x) for x in blackdata[list_num]]#数据从字符串转化为浮点，便于之后的计算
            blackdatafinal.append(blackdata[list_num]) #生成加工后的最终的训练数据


        finalCluster,finalCenters = hcluster(traindatafinal, len(traindatafinal)//40)#聚类，根据聚类数据集大小决定聚类数量，平均每40条数据为一类
        maxDists,allDists=maxdists(finalCluster,finalCenters)#计算离聚类中心的最大距离和所有距离
        finalThres=besthres(blackdatafinal,allDists,maxDists,finalCenters)#计算最佳阈值

        #print("聚类结果：")
        #print(finalCluster)
        print("对应的聚类中心：")
        print(finalCenters)
        print("对应的离聚类中心的最大距离：")   
        print(maxDists)
        #print("对应的离聚类中心的所有距离：")   
        #print(allDists)        
        print("阈值：")  
        print(finalThres)

    with open("E:\\dm\\centers1.csv", "w",newline= '') as csvFile:     # 保存聚类中心为文件，newline= '' 是为了控制csv存入的时候的空行问题
         csvWriter = csv.writer(csvFile)
         for data in finalCenters:
             csvWriter.writerow(data)
    with open("E:\\dm\\thresholds1.csv", "w",newline= '') as csvFile:     #保存阈值为文件
         csvWriter = csv.writer(csvFile)
         csvWriter.writerow(finalThres)
         #csvWriter.writerow(maxDists)#直接用最大距离作为阈值










    



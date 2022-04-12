#四种方法的平均误差距离

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import networkx as nx
import os
import random
from itertools import islice
import torch
from scipy.sparse.coo import coo_matrix
import argparse
import math
from random import choice
import community as community_louvain
from collections import Counter
import collections
#底图
#G = nx.scale_free_graph(400)
# BA=nx.random_graphs.barabasi_albert_graph(1000,3)
# G = nx.Graph(BA)
N=500
fname = "food500"
G = nx.read_edgelist('./'+fname+'_weight.txt',nodetype = int,data=(('weight',float),),create_using=nx.Graph())
# pos=nx.spring_layout(G) 
# nx.draw(G,pos)
# plt.show()
#病毒图
#SI模型
part = 0.1  #BA5000节点时，part=0.05时，病毒图大小约为400左右
graph_labels = []
def genGraph(sn,datadir,bmname):

#感染过程
    node = list(map(int,G.nodes))#图中节点列表，元素转化为整数型
    S = node
    I = []

    j=0
    while j<1:
        #start_node = random.choice(node)#1个初始感染节点
        start_node = sn#1个初始感染节点
        I.append(start_node)
        S.remove(start_node)
        j=j+1
    
    print(start_node)
    
    new_G_small = nx.Graph()
    count = [1]
    statechange = []
    edgechange = []
    edgeweight = []
    weight_s = 1
    #for i in range(Roundtime):
    while len(I)<=part*len(G.nodes()):
        for nbr, datadict in G.adj.items():#遍历G的所有节点，nbr节点名称，datadict与节点相连的边
            if int(nbr) in S:
                node_adj = 0               #S节点的感染邻接点数
                for key in datadict:
                    if int(key) in I:
                        node_adj=node_adj+1
                        edgechange.append(int(key))
                        edgeweight.append(G.get_edge_data(int(nbr),int(key))['weight'])
                for weight in edgeweight:
                    weight_s = weight_s*(1-weight)
                rate = 1-weight_s
                if random.random() <= rate:   #被感染后，节点状态变化，感染图的边增加（周围所有感染节点与该点的连边都算上）
                    for a in edgechange:
                        new_G_small.add_edge(int(nbr),a)
                    statechange.append(int(nbr))
                edgechange = []
                edgeweight=[]
                weight_s=1 
        for i in statechange:
            S.remove(i)
            I.append(i)
        count.append(len(I))
        statechange = []
    perfix = os.path.join(datadir,bmname)
    filename_discen = perfix + '_discen.txt'
    # new_G = nx.Graph()
    # new_G.add_nodes_from(i for i in range(N))
    # new_G.add_edges_from(new_G_small.edges())
    #distance centrality
    if not nx.is_empty(new_G_small):
        dis_path = dict(nx.shortest_path_length(new_G_small))
        dis_d={}
        for k,v in dis_path.items():
            dis_s=0
            for i in v.values():
                dis_s = dis_s+i
            dis_d[k] = dis_s
        distance_centrality = min(dis_d, key=lambda x: dis_d[x]) 
        with open(filename_discen,'a') as discenf:
            discenf.write(str(distance_centrality))
            discenf.write('\n')
        #print(distance_centrality)
        graph_labels.append(start_node)
def graph_label(datadir,bmname):
    perfix = os.path.join(datadir,bmname)
    filename_graph_labels = perfix+ '_graph_labels.txt'
    with open(filename_graph_labels,'w') as f:
        for i in graph_labels:
            f.write(str(i))
            f.write('\n')
def data_A(datadir,bmname):
    #perfix = os.path.join(datadir,bmname)
    graphs=1
    nodehead=0
    nodetail=1000
    for nodesn in range(nodehead,nodetail):
        for j in range(graphs):
            genGraph(nodesn,datadir,bmname)
#频率分布直方图





def main():

    bmname = 'food500_nSI_z0.1_m70_p0.8_d1'
    #path = os.path.join('/home/zhang/Documents/pytorch/learn/GraphKernel/rexying_diffpool/diffpool-master/data',bmname)
    path = os.path.join('/home/iot/zcy/usb/copy/rexying_diffpool/diffpool-master/data',bmname)
    #path1 = os.path.join('/home/iot/zcy/usb/copy/rexying_diffpool/diffpool-master/labels',bmname)
    if not os.path.exists(path):
        os.makedirs(path)
    #perfix = os.path.join(path,bmname)
    # data_A(path,bmname)
    # graph_label(path,bmname)
    labels = []
    discen = []
    jordancenter =[]
    unbet = []
    discen = []
    dynage = []
    labels_small = []
    preds_small =[]
    file_labels = path +'/'+bmname + '_graph_labels.txt'
    file_discen = path + '/'+bmname + '_discen.txt'
    file_val_jordancenter = path+ '/'+bmname  + '_jordancenter.txt'
    file_unbet = path+ '/'+bmname   + '_unbet.txt'
    file_discen = path + '/'+bmname  + '_discen.txt'
    file_dynage = path+ '/'+bmname   + '_dynage.txt'
    #file_labels_small = path1+ '_labels.txt'
    #file_preds_small = path1 + '_preds.txt'
    with open(file_labels,'r') as f1:
        for line in f1.readlines():
            labels.append(int(line.strip('\n')))
    with open(file_val_jordancenter,'r') as f3:
        for line in f3.readlines():
            jordancenter.append(int(line.strip('\n')))
    with open(file_unbet,'r') as f4:
        for line in f4.readlines():
            unbet.append(int(line.strip('\n')))
    with open(file_discen,'r') as f5:
        for line in f5.readlines():
            discen.append(int(line.strip('\n')))
    with open(file_dynage,'r') as f6:
        for line in f6.readlines():
            dynage.append(int(line.strip('\n')))

    # with open(file_labels_small,'r') as f7:
    #     for line in f7.readlines():
    #         labels_small.append(int(line.strip('\n')))
    # with open(file_preds_small,'r') as f2:
    #     for line in f2.readlines():
    #         preds_small.append(int(line.strip('\n')))
    read_dic = np.load(fname+"_short_path.npy",allow_pickle = True).item()

    # distance_preds =[]#预测值与真实值之间的距离
    # sum1=0
    # for i in range(len(labels_small)):
    #     a = read_dic[labels_small[i]][preds_small[i]]
    #     distance_preds.append(a)
    #     sum1=sum1+a
    # average_distance_preds = sum1/(len(distance_preds))
    # print('预测值与真实值之间的距离：',distance_preds)
    # print('平均预测距离：{:.4}'.format(average_distance_preds))
    # result = {}
    # for i in set(distance_preds):
    #     result[i] = distance_preds.count(i)
    # #print(result[1]+result[0])

    distance_center=[]#真实值与约旦中心的距离
    #print(nx.eccentricity(G))#G中所有节点的离心率
    #print(nx.radius(G))#G的半径，离心率等于半径的点称为图的约旦中心（中心）
    sum2= 0
    for i in range(len(labels)):
        b = read_dic[labels[i]][jordancenter[i]]
        distance_center.append(b)
        sum2 = sum2+b
    average_distance_center = sum2/(len(distance_center))
    #print('约旦中心与真实值之间的距离：',distance_center)
    print('平均约旦距离：{:.4}'.format(average_distance_center))

    distance_unbet=[]#真实值与无偏中心性的距离
    sum4= 0
    for i in range(len(labels)):
        b = read_dic[labels[i]][unbet[i]]
        distance_unbet.append(b)
        sum4 = sum4+b
    average_distance_unbet = sum4/(len(distance_unbet))
    #print('无偏中心性与真实值之间的距离：',distance_unbet)
    print('平均无偏中心性距离：{:.4}'.format(average_distance_unbet))

    distance_discen=[]#真实值与距离中心的距离
    sum3= 0
    for i in range(len(labels)):
        b = read_dic[labels[i]][discen[i]]
        distance_discen.append(b)
        sum3 = sum3+b
    average_distance_discen = sum3/(len(distance_discen))
    #print('距离中心与真实值之间的距离：',distance_discen)
    print('平均距离中心距离：{:.2}'.format(average_distance_discen))
    # count = 0
    # for i in range(len(distance_preds)):
    #     if distance_preds[i] <= distance_discen[i]:
    #         count=count+1
    # print('预测距离小于等于距离中心距离个数：',count)
    #画出距离中心频率直方图
    distance_dynage=[]#真实值与动态年龄的距离
    sum5= 0
    for i in range(len(labels)):
        b = read_dic[labels[i]][dynage[i]]
        distance_dynage.append(b)
        sum5 = sum5+b
    average_distance_dynage = sum5/(len(distance_dynage))
    #print('动态年龄与真实值之间的距离：',distance_dynage)
    print('平均动态年龄距离：{:.4}'.format(average_distance_dynage))

    # #画出预测值频率直方图
    # distance_preds_sequence = sorted([d for d in distance_preds], reverse=True)  # distance sequence
    # distance_predsCount = collections.Counter(distance_preds_sequence)
    # dis_preds, cnt = zip(*distance_predsCount.items())
    # # dis_preds1=[]
    # # for i in dis_preds:
    # #     dis_preds1.append(i)
    # #     dis_preds1.append(2)
    # #     dis_preds1.append(3)
    # dis_preds_frequence = []
    # for i in cnt:
    #     dis_preds_frequence.append(i/(len(preds_small)))
    # #fig, ax = plt.subplots()
    # plt.figure()
    # ax1 = plt.subplot(3,2,1)
    # plt.bar(dis_preds, dis_preds_frequence, width=0.10, color="b")

    # #plt.title("Distance_preds Histogram")
    # plt.ylabel("Frequence")
    # plt.xlabel("Distance_preds")
    # plt.ylim((0,1))
    # ax1.set_xticks([d for d in dis_preds])
    # ax1.set_xticklabels(dis_preds)


    #画出约旦中心频率直方图
    distance_center_sequence = sorted([d for d in distance_center], reverse=True)  # distance_center sequence
    distance_centerCount = collections.Counter(distance_center_sequence)
    dis_center, center_cnt = zip(*distance_centerCount.items())
    dis_center_frequence = []
    for i in center_cnt:
        dis_center_frequence.append(i/(len(distance_center)))
    ax2 = plt.subplot(3,2,2)
    plt.bar(dis_center, dis_center_frequence, width=0.1, color="g")

    plt.title("Jordan Center Histogram")
    plt.xlabel("Jordan Center")
    plt.ylim((0,1))
    ax2.set_xticks([d for d in dis_center])
    ax2.set_xticklabels(dis_center)
    #画出无偏中心性频率直方图
    distance_unbet_sequence = sorted([d for d in distance_unbet], reverse=True)  # distance_center sequence
    distance_unbetCount = collections.Counter(distance_unbet_sequence)
    dis_unbet, center_cnt = zip(*distance_unbetCount.items())
    dis_unbet_frequence = []
    for i in center_cnt:
        dis_unbet_frequence.append(i/(len(distance_unbet)))
    ax2 = plt.subplot(3,2,3)
    plt.bar(dis_unbet, dis_unbet_frequence, width=0.1, color="g")

    plt.title("Unbiased Betweenness Histogram")
    plt.xlabel("Distance_unbet")
    plt.ylim((0,1))
    ax2.set_xticks([d for d in dis_unbet])
    ax2.set_xticklabels(dis_unbet)

    #画出距离中心频率直方图
    distance_discen_sequence = sorted([d for d in distance_discen], reverse=True)  # distance_center sequence
    distance_discenCount = collections.Counter(distance_discen_sequence)
    dis_discen, center_cnt = zip(*distance_discenCount.items())
    dis_discen_frequence = []
    for i in center_cnt:
        dis_discen_frequence.append(i/(len(distance_discen)))
    ax2 = plt.subplot(3,2,4)
    plt.bar(dis_discen, dis_discen_frequence, width=0.1, color="g")

    plt.title("Distance Center Histogram")
    plt.xlabel("Distance_discen")
    plt.ylim((0,1))
    ax2.set_xticks([d for d in dis_discen])
    ax2.set_xticklabels(dis_discen)

    #画出动态年龄频率直方图
    distance_dynage_sequence = sorted([d for d in distance_dynage], reverse=True)  # distance_center sequence
    distance_dynageCount = collections.Counter(distance_dynage_sequence)
    dis_dynage, center_cnt = zip(*distance_dynageCount.items())
    dis_dynage_frequence = []
    for i in center_cnt:
        dis_dynage_frequence.append(i/(len(distance_dynage)))
    ax2 = plt.subplot(3,2,5)
    plt.bar(dis_dynage, dis_dynage_frequence, width=0.1, color="g")

    plt.title("Dynamic Age Histogram")
    plt.xlabel("Distance_dynage")
    plt.ylim((0,1))
    ax2.set_xticks([d for d in dis_dynage])
    ax2.set_xticklabels(dis_dynage)
    #保存图片
    path_fig = os.path.join('/home/iot/zcy/usb/copy/research/graph_python/research/experiments_graph',bmname) + '_results.png'
    plt.tight_layout()
    plt.savefig(path_fig)
    plt.show()


if __name__ == "__main__":
    main()
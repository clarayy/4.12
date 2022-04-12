#SI模型，不完全观测，邻接矩阵的生成
#邻接矩阵考虑权重，结果不同

#新的感染图画法，添加边根据所有感染节点来增加
#propagation_pro1.py的升级
#给边增加权重，随机增加
#改为传播到总结点数的0.8停止传播
#propagation使用的是从I开始遍历，使S改变状态
#本程序从S开始遍历，感染概率为1-（1-q）^n
#在一张图上同时显示初始图结构和传播感染图，即传播感染图是初始图结构的一部分
#from research.new_propagation_SI import InfectionRate, Roundtime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import networkx as nx
import os
import random
from itertools import islice
import argparse

N =62
name = "dolphins"
# B = np.load(name+".npy")#读取固定的图
# G = nx.Graph(B)
G = nx.read_edgelist('./'+name+'_weight.txt',nodetype = int,data=(('weight',float),),create_using=nx.Graph())

InfectionRate = 0.1#概率太大，10轮感染1400个节点
Roundtime =3
obn = int(N*0.5)  #有一半的节点可以观测到
observenode = random.sample(range(0,N-1),obn)#每次都随机选还是固定呢
#observenode= [i for i in range(62)]
print(obn,observenode)
U=[]
for i in range(N):
    if i not in observenode:
        U.append(i)
print(U)
#感染过程
node = list(map(int,G.nodes))#图中节点列表，元素转化为整数型
#node1 = list(set(node))#节点元素从小到大排序
#print(len(node))
S = node
I = []

j=0
while j<1:
    #start_node = random.choice(node)#1个初始感染节点
    start_node = 0#1个初始感染节点
    I.append(start_node)
    S.remove(start_node)
    j=j+1
print("start_node:")
print(start_node)
part = 0.5
new_G = nx.Graph()
new_G_duizhao = nx.Graph()
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
                # for a in edgechange:
                #     new_G.add_edge(int(nbr),a)
                statechange.append(int(nbr))
            edgechange = []
            edgeweight=[]
            weight_s=1      
    for i in statechange:
        S.remove(i)
        I.append(i)
    if len(I)==1:
        break
    count.append(len(I))
    statechange = []
ob_I=[]
ob_S=[]
for i in observenode:
    if i in I:
        ob_I.append(i)
    else:
        ob_S.append(i)
print(len(ob_I)+len(ob_S)+len(U))
for nbr, datadict in G.adj.items():
    if int(nbr) in ob_I:
        for key in datadict:
            if int(key) in ob_I:
                new_G.add_edge(int(nbr),int(key),weight=6)
            elif int(key) in ob_S:
                new_G.add_edge(int(nbr),int(key),weight=3)
            elif int(key) in U:
                new_G.add_edge(int(nbr),int(key),weight=4)
    elif int(nbr) in ob_S:
        for key in datadict:
            if int(key) in ob_S:
                new_G.add_edge(int(nbr),int(key),weight=0)
            elif int(key) in U:
                new_G.add_edge(int(nbr),int(key),weight=1)
    elif int(nbr) in U:
        for key in datadict:
            if int(key) in U:
                new_G.add_edge(int(nbr),int(key),weight=2)
A = nx.to_numpy_matrix(new_G)   #
print("A:",A)
#print(G.edges())
plt.figure()
Innum = plt.subplot(111)
props = {'title':'Total number of Infected Users',
          'ylabel':'number','xlabel':'time'}
Innum.set(**props)
x = []
for i in range(0,len(count)):
    x.append(i)
Innum.plot(x,count)
Innum.text(0,0,'N:%.0f,Rate:%.4f' %(N,InfectionRate))
print('len(I):',len(I))
print("I=",I)
plt.show()  #显示感染曲线
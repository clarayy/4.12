#与ob_B_SI.py的区别是，没有连接所有可观测节点相连的边(按照实际情况，不知道感染来源，所以需要连接所有边)
#不完全观测的程序
#添加观测到的节点相连的边
#权重作为感染率，单张图，参考propagation_pro1_4.py和5_jian_pro_SI_obser.py

#生成一张病毒图的SI模型程序
#基于propagation_pro1_3.py上改进
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
#变量：B，sn范围,每个sn张数 ，Infectionrate, Roundtime，data文件名
N = 62#记得必须改
fname = "dolphins"
G = nx.read_edgelist('./'+fname+'_weight.txt',nodetype = int,data=(('weight',float),),create_using=nx.Graph())

part=0.1
Roundtime = 3

obn = int(N*0.5)  #有一半的节点可以观测到
observenode = random.sample(range(0,N-1),obn)
observenode= [0, 1,2,3, 4,5, 9, 10,11, 12]
print(obn,observenode)

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
new_G = nx.Graph()
sub_new_G = nx.Graph()   ##
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
                    #new_G.add_edge(int(nbr),a)
                    if int(nbr) in observenode:    #情况A+C   ##
                        sub_new_G.add_edge(a,int(nbr))         ##
                statechange.append(int(nbr))
            edgechange = []
            edgeweight=[]
            weight_s=1            
    for i in statechange:
        S.remove(i)
        I.append(i)
    for nbr, datadict in G.adj.items():
        if int(nbr) in I:
            for key in datadict:
                if int(key) in I:
                    new_G.add_edge(int(nbr),int(key))
    if len(I)==1:
        break
    count.append(len(I))
    statechange = []

plt.figure()
Innum = plt.subplot(111)
props = {'title':'Total number of Infected Users',
          'ylabel':'number','xlabel':'time'}
Innum.set(**props)
x = []
for i in range(0,len(count)):
    x.append(i)
Innum.plot(x,count)
#Innum.text(0,0,'N:%.0f,Rate:%.4f' %(N,InfectionRate))
Innum.text(0,0,'N:%.0f' %N)
print("I=",I)
print('len(I):')
print(len(I))
plt.show()  #显示感染曲线

#nx.draw(new_G)
pos = nx.spring_layout(new_G) #为什么报错！！！！！！！！！！
nx.draw(new_G,pos,with_labels = True)#逗号是中文的  #画图
plt.show()

#在一张图上显示
Gt=new_G.copy()
for node in I:
    if node!= start_node:
        Gt.remove_node(node)
#print(len(Gt.nodes()))#源节点
#print(len(G.nodes()))
pos = nx.spring_layout(G)
nx.draw(G,pos,node_color='b',node_size=1,edge_color = 'b',with_labels=True)
nx.draw_networkx_nodes(new_G,pos,node_color='r',node_size=1)
nx.draw_networkx_edges(new_G,pos,edge_color = 'r')
nx.draw_networkx_nodes(sub_new_G,pos,node_color='y',node_size=1)
nx.draw_networkx_edges(sub_new_G,pos,edge_color = 'y')
nx.draw(Gt,pos,node_color = 'g',node_size = 10)
plt.show()
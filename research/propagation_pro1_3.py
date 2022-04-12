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

# parser = argparse.ArgumentParser(description='SI for argparse')
# parser.add_argument('--Number', '-N', help='总数 属性，非必要参数',required=True)
# parser.add_argument('--name', '-n', help='底图名称，有默认值',required=True)
# parser.add_argument('--Infection', '-g', help='感染率，有默认值',default=0.5)
# parser.add_argument('--Roundtime', '-r', help='轮数，必要参数', default=4)
# args = parser.parse_args()

# N = args.Number
# name = args.name
# InfectionRate = args.Infection
# Roundtime = args.Roundtime
# print(args.Number,args.name,args.Infection,args.Roundtime)
N = 20
name = "BA20_3"
# B = np.load(name+".npy")#读取固定的图
# G = nx.Graph(B)
G = nx.read_edgelist('./'+name+'_weight.txt',nodetype = int,data=(('weight',float),),create_using=nx.Graph())
# for u,v in G.edges():
#     G.add_edge(u,v,weight=random.random())
# print(G.edges(data=True))
# pos=nx.spring_layout(G)
# print(G.edges(data=True))
# nx.draw(G,pos,node_size=1,with_labels = True)
# plt.show()
InfectionRate = 0.1#概率太大，10轮感染1400个节点
Roundtime = 2
'''
#测试用的小图
N = 34
filename = '/home/zhang/Documents/research/graph_python/research/graphtest.txt'
G = nx.Graph()
with open(filename,'r') as file:
    for line in file:
        head,tail=[str(x) for x in line.split( )]
        G.add_edge(head,tail)
#nx.draw(G,with_labels = True)
#plt.show()
'''

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
count = [1]
statechange = []
edgechange = []
edgeweight = []
weight_s = 1
for i in range(Roundtime):
#while len(I)<=part*len(G.nodes()):
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
                    new_G.add_edge(int(nbr),a)
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

#显示源节点
#存储边数据
#nx.write_edgelist(new_G,'data_G1.txt',delimiter=',',data = False)
#print(new_G.edges())
#print(len(new_G.edges()))
print('len(new_G.nodes()):')
print(len(new_G.nodes()))
print('edges:')
print(new_G.edges())

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
nx.draw(Gt,pos,node_color = 'red',node_size = 10)
plt.show()

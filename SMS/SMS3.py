import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import networkx as nx
import os
import random
from itertools import islice
#使用Cckun数据作为newokx，加上R状态
#初始节点为10，toI概率0.0046，toM概率0.01，循环的判断条件改一下
#免疫率就是感染率，0.0046与0.9954？

filename='E:/python/ncckun.csv'
G=nx.Graph()

with open(filename) as file:
    for line in file:
        time,head,tail=[str(x) for x in line.split(',')]#读取csv文件改动部分
        G.add_edge(head,tail)

     
node = list(map(int,G.nodes))#图中节点列表，元素整数型
node1 = list(set(node))#节点元素从小到大排序
print(len(node))
S = node
E = []
I = []
M = []
TP01 = 0.1
TP00 = 0.9
TP10 = 0.3
TP12 = 0.7
TP13 = 1
a = 0.0046
j=0
while j<10:
    start_node = random.choice(node)#1个初始感染节点
    I.append(start_node)
    S.remove(start_node)
    j=j+1

print(I)

'''
for key,value in G.adj.items():#一般字典循环
    for i in I:
        i=str(i)
        if i == key:
            d = G.adj[key]
            print(d.keys)
for nbr, foovalue in G[node].data('foo', default=1):#G.adj邻接矩阵里的数据
    print(nbr,foovalue)
'''
count = [1]
time = [1]
stateStoI = []
stateStoM = []
while len(I)<1800:
#for i in range(100):
    for nbr, datadict in G.adj.items():#遍历G的所有节点，nbr节点名称，datadict与节点相连的边
        if int(nbr) in I:
            for key in datadict:
                if int(key) in S:
                    rate=random.random()
                    if rate <= 0.0046:
                        stateStoI.append(int(key))
                    elif rate <= 0.0092:#转变成为R的概率为0.0046--0.0146,假设
                        stateStoM.append(int(key))
    stateStoI1=list(set(stateStoI))
    stateStoM1=list(set(stateStoM))
    for v in stateStoM1:
        if v in stateStoI1:
            stateStoM.remove(v)
    for i in stateStoI1:
        I.append(i)
        if i in S:
            S.remove(i)
    for i in stateStoM1:
        M.append(i)
        if i in S:#试试不要这句判断
            S.remove(i)
    count.append(len(I))
    stateStoI = []                   
    stateStoM = []
         
fig = plt.figure()
Innum = fig.add_subplot()
Innum.set(title='Total number of Infected Users',
          ylabel='number',xlabel='time')
x = []
for i in range(0,len(count)):
    x.append(i)
Innum.plot(x,count)
print(x[:5])
print(count[:5])
print('M:')
print(M[:10])
plt.show()

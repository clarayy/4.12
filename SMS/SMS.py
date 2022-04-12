import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import networkx as nx
import os
import random
from itertools import islice
#以node2vec为例，加上R状态
os.chdir('E:\python')
filename='node2vec.txt'
G=nx.Graph()

with open(filename) as file:
    for line in file:
        head,tail=[str(x) for x in line.split( )]
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
while j<1:
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
#while len(I)<34:
for i in range(10):
    for nbr, datadict in G.adj.items():#遍历G的所有节点，nbr节点名称，datadict与节点相连的边
        if int(nbr) in I:
            for key in datadict:
                if int(key) in S:
                    rate=random.random()
                    if rate <= 0.3:
                        stateStoI.append(int(key))
                    elif rate <= 0.5:#转变成为R的概率为0.0046--0.0146,太小了，数据太少，为直线
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
#        if i in S:#试试不要这句判断
#           S.remove(i)
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
print('R:')
print(M)
print(I)
print(S)
plt.show()

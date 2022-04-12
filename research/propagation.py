import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import networkx as nx
import os
import random
from itertools import islice

N = 2000
B = np.load("A.npy")#读取固定的图
G = nx.Graph(B)
#感染过程
node = list(map(int,G.nodes))#图中节点列表，元素转化为整数型
node1 = list(set(node))#节点元素从小到大排序
print(len(node))
S = node
I = []

'''
a = 0.0046
'''
j=0
while j<1:
    #start_node = random.choice(node)#1个初始感染节点
    start_node=8
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
statechange = []
InfectionRate = 0.46
Roundtime = 20
for i in range(Roundtime):
#while len(I)<300:
    for nbr, datadict in G.adj.items():#遍历G的所有节点，nbr节点名称，datadict与节点相连的边
        if int(nbr) in I:
            for key in datadict:
                if int(key) in S:
                    if random.random() <= InfectionRate:
                        statechange.append(int(key))#如果被不同节点感染，则节点重复，怎么算
    statechange1=list(set(statechange))
    for i in statechange1:
        I.append(i)
        if i in S:
            S.remove(i)
    count.append(len(I))
    statechange=[]                   
    
         
plt.figure()
Innum = plt.subplot(111)
props = {'title':'Total number of Infected Users',
          'ylabel':'number','xlabel':'time'}
Innum.set(**props)
x = []
for i in range(0,len(count)):
    x.append(i)
Innum.plot(x,count)
Innum.text(40,250,'N:%.0f,Rate:%.4f' %(N,InfectionRate))
print(x[:5])
print(len(I))
plt.show()
#0.0046应该换成1-(1-q)^n 受感染的概率与邻节点感染节点的数量有关。但可知：每个
#节点每个时间点的邻节点都不一样，需要遍历。怎么与图遍历算法结合。

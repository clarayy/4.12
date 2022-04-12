import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import networkx as nx
import os
import random
from itertools import islice
#生成scale_free网络，节点数400
#G = nx.scale_free_graph(40000)
#循环次数100，感染概率0.046

#a model for social network复现

G = nx.path_graph(30)#从30个节点单链开始
new_node=30
while new_node <40000:
    
    node = list(map(int,G.nodes))#图中节点列表，元素整数型

    init_node = []
    adj_node = []
    snd_node = []
    add_node = []
    p = random.random()
    if p<0.95:
        init_node.append(random.choice(node))
    else:
        init_node.extend(random.sample(node,2))
    for n, nbrs in G.adj.items():
        if n in init_node:
            for key in nbrs:
                adj_node.append(int(key))#添加第二层节点
    p2 = random.random()
    if p2<(1/4):
        k=0
    elif p2<(1/2):
        k=1
    elif p2<(3/4):
        k=2
    elif p2<1:
        k=3
    G.add_node(30)#添加节点
    add_node.extend(init_node)
    if k<=len(adj_node):
        add_node.extend(random.sample(adj_node,k))
    else:
        add_node.extend(adj_node)
    for n in add_node:
        G.add_edge(new_node,n)
    new_node=new_node+1
#pos=nx.spring_layout(G) 
#nx.draw(G,pos,node_size=10)
#nx.write_gexf(G,'28social_network_400000.gexf')
print('a')
#plt.show()
         
node = list(map(int,G.nodes))#图中节点列表，元素转化为整数型
node1 = list(set(node))#节点元素从小到大排序
print(len(node))
S = node
E = []
I = []
M = []
'''
TP01 = 0.1
TP00 = 0.9
TP10 = 0.3
TP12 = 0.7
TP13 = 1
a = 0.0046
'''
j=0
while j<10:
    start_node = random.choice(node)#10个初始感染节点
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
for i in range(500):
#while len(I)<300:
    for nbr, datadict in G.adj.items():#遍历G的所有节点，nbr节点名称，datadict与节点相连的边
        if int(nbr) in I:
            for key in datadict:
                if int(key) in S:
                    if random.random() <= 0.0046:
                        statechange.append(int(key))
    statechange1=list(set(statechange))
    for i in statechange1:
        I.append(i)
        if i in S:
            S.remove(i)
    count.append(len(I))
    statechange=[]                   
    
         
fig = plt.figure()
Innum = fig.add_subplot()
Innum.set(title='Total number of Infected Users',
          ylabel='number',xlabel='time')
x = []
for i in range(0,len(count)):
    x.append(i)
Innum.plot(x,count)
print(x[:5])
print(len(I))
plt.show()
#0.0046应该换成1-(1-q)^n 受感染的概率与邻节点感染节点的数量有关。但可知：每个
#节点每个时间点的邻节点都不一样，需要遍历。怎么与图遍历算法结合。

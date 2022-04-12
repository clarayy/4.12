import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import networkx as nx
import os
import random
import collections
#a model for social network复现

G = nx.path_graph(30)#从30个节点单链开始
new_node=30
while new_node <2000:
    
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

H = nx.path_graph(30)#从30个节点单链开始
new_node=30
while new_node <2000:
    
    node = list(map(int,H.nodes))#图中节点列表，元素整数型

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
    if p2<(1/3):
        k=0
    elif p2<(2/3):
        k=1
    elif p2<1:
        k=2
    H.add_node(30)#添加节点
    add_node.extend(init_node)
    if k<=len(adj_node):
        add_node.extend(random.sample(adj_node,k))
    else:
        add_node.extend(adj_node)
    for n in add_node:
        H.add_edge(new_node,n)
    new_node=new_node+1
#度分布
degree =[]
p = []#理论值
p1 = []#理论值
for n, d in G.degree():
    k=d**(-1.5)
    k1=pow(d,-2)
    degree.append(d)
    p.append(k)
    p1.append(k1)

degree_sequence=sorted(degree,reverse=True)
H_degree_sequence = sorted([d for n, d in H.degree()], reverse=True) 
H_degreeCount = collections.Counter(H_degree_sequence)
H_deg, H_cnt = zip(*H_degreeCount.items())
#实际值

degreeCount = collections.Counter(degree_sequence)
deg, cnt = zip(*degreeCount.items())
pcnt=[]
for i in cnt:
    pcnt.append(i/2000)

H_pcnt=[]
for i in H_cnt:
    H_pcnt.append(i/2000)
fig1, ax1 = plt.subplots()
ax1.set_xscale("log")
ax1.set_yscale("log")
ax1.set_xlim(1e0, 1e3)
ax1.plot(degree,p)#理论值
ax1.plot(degree,p1,c='yellow')#理论值
#fig2, ax2 = plt.subplots()
ax1.scatter(deg,pcnt, s=5,c='red')#论文中情况2的实际值
ax1.scatter(H_deg,H_pcnt, s=5,c='purple')#情况3的实际值
#plt.loglog(p,degree_sequence)
plt.title("Degree distributions")
plt.ylabel("p(k)")
plt.xlabel("degree")
print(deg[:5])
print(pcnt[:5])
y2 = []
for i in range(len(deg)):
    y2.append(pcnt[i]/(deg[i]**(-1.5)))
y3 = []
for i in range(len(H_deg)):
    y3.append(H_pcnt[i]/(H_deg[i]**(-1.5)))
# draw graph in inset
ax2=fig1.add_axes([0.6, 0.6, 0.3, 0.3])
ax2.set_xscale('log')
ax2.set_xlim(1e0,1e2)
ax2.scatter(deg,y2,s=5)
ax2.scatter(H_deg,y3,s=5,c='yellow')
plt.show()

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
    
#聚类系数分析
clu=[]
deg=[]
k=[]
simulation= []
for v in nx.nodes(G):
    if nx.degree(G,v) not in k:
        clu.append(nx.clustering(G,v))#聚类实际值
        deg.append(nx.degree(G,v))
        k.append(nx.degree(G,v))
        simulation.append(2.3/(nx.degree(G,v)))
H_clu=[]
H_deg=[]
H_k=[]
H_simulation= []
for v in nx.nodes(H):
#    if nx.degree(H,v) not in H_k:
    H_clu.append(nx.clustering(H,v))#聚类实际值
    H_deg.append(nx.degree(H,v))
    H_k.append(nx.degree(H,v))
    H_simulation.append(3.5/(nx.degree(H,v)))
fig, ax = plt.subplots()
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_ylim(1e-3,1e1)
ax.scatter(deg,clu,s=5,c='blue')
ax.plot(deg,simulation)
ax.scatter(H_deg,H_clu,s=5,c='red')
ax.plot(H_deg,H_simulation,c='purple')
plt.show()



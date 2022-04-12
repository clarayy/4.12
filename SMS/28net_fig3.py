import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import random
#a model for social network复现  fig3

G = nx.path_graph(30)#从30个节点单链开始
new_node=30
while new_node <1000:
    
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

pos=nx.spring_layout(G) 
nx.draw(G,pos,node_size=10)
#nx.write_gexf(G,'28social_network_400000.gexf')

A = nx.to_numpy_matrix(G)#邻接矩阵
print(A)
plt.show()

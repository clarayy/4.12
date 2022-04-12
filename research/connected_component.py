#在得到的传播图为非完全连通子图时的其他四种方法的改进
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

B=np.load("unconnected.npy")
new_G_small = nx.Graph(B)

# #无偏中介中心性
# #非连通子图也可以求
# bet_cen = nx.betweenness_centrality(new_G_small)#节点的中介中心性,一个顶点出现在其他任意两个顶点队之间的最短路径的次数
# deg = new_G_small.degree()#节点的度
# ub={}
# for i in bet_cen.keys():
#     if deg[i]!=0:
#         ub[i] = bet_cen[i]/(math.pow(deg[i],0.85))
# unbiased_betweenness = max(ub, key=lambda x: ub[x])
# print(bet_cen)
# print(ub)
# print(unbiased_betweenness)

# #distance centrality 
# #从相等的最短路径中，选节点标签最小的一个。   不一定，随机选的吧
# p = dict(nx.shortest_path_length(new_G_small))
# d={}
# for k,v in p.items():
#     s=0
#     for i in v.values():
#         s = s+i
#     d[k] = s
# distance_centrality = min(d, key=lambda x: d[x])
# print(p)
# print(distance_centrality)

#dynamic ages
#非连通子图也可以计算，去掉断开子图的节点后，对图的邻接矩阵的特征值影响为0；选择影响最大的为dynage
frozen_graph = nx.freeze(new_G_small)#G被冷冻为frozen_graph，不会改变
unfrozen_graph = nx.Graph(frozen_graph)#删除节点在非冷冻图上进行，冷冻图不变
AS = nx.adjacency_spectrum(frozen_graph)#邻接矩阵特征值

m = np.real(AS).round(4).max()
all_nodes = new_G_small.nodes

da = {}                             ###!!!!!字典才对
for i in all_nodes:
    unfrozen_graph.remove_node(i)
    AS1 = nx.adjacency_spectrum(unfrozen_graph)
    m1 = np.real(AS1).round(4).max()
    da[i] = float(format(abs(m-m1)/m,'.4f'))   #单独运算看对不对
    unfrozen_graph = nx.Graph(frozen_graph)
dynage = max(da, key=lambda x: da[x])
print(AS)
print(all_nodes)
print(dynage)
# frozen_graph = nx.freeze(new_G_small)#G被冷冻为frozen_graph，不会改变
# unfrozen_graph = nx.Graph(frozen_graph)#删除节点在非冷冻图上进行，冷冻图不变
# Gc_node = max(nx.connected_components(new_G_small), key=len)   #sub_newG的最大连通子图来求Jordan Center
# print(Gc_node)
# Gc = unfrozen_graph.subgraph(Gc_node)    #改变了new_G_small，使其成为最大连通子图
# Jordan_center  = nx.center(Gc)
# print(Jordan_center)
nx.draw(new_G_small,with_labels =True)
plt.show()
# nx.draw(Gc,with_labels =True)
# plt.show()
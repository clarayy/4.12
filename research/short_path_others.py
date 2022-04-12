#其他的一些图的中心性
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import networkx as nx
import os
import random
from itertools import islice
from collections import Counter
import collections
import math
#tribes N=16
#dolphins N=62
#N = 50
fname = 'WS500'
B = np.load(fname+".npy")#读取固定的图d 的邻接矩阵
G = nx.DiGraph(B)
#print(G.nodes())
print("G.edges()数量:",len(G.edges()))
# nx.draw(G,with_labels = True)
# plt.show()
p= dict(nx.shortest_path_length(G))
#print(p[499][999])
np.save(fname+"_short_path.npy",p)
""" #无偏中介中心性
bet_cen = nx.betweenness_centrality(G)#节点的中介中心性
deg = G.degree()#节点的度
ub=[]
for i in range(N):
    ub.append(bet_cen[i]/(math.pow(deg[i],0.85)))
unbiased_betweenness = ub.index(max(ub)) """
#distance centrality
# p = dict(nx.shortest_path_length(G))
# d=[]
# for k,v in p.items():
#     s=0
#     for i in v.values():
#         s = s+i
#     d.append(s)
# print(d)
# distance_centrality = d.index(min(d))
# print(distance_centrality)
""" #dynamic ages
frozen_graph = nx.freeze(G)#G被冷冻为frozen_graph，不会改变
unfrozen_graph = nx.Graph(frozen_graph)#删除节点在非冷冻图上进行，冷冻图不变
AS = nx.adjacency_spectrum(frozen_graph)#邻接矩阵特征值
#print(np.real(AS).round(2).max())#numpy的实数部分,两位小数，最大值
m = np.real(AS).round(2).max()
all_nodes = G.nodes
#print(all_nodes)
da = []
for i in all_nodes:
    unfrozen_graph.remove_node(i)
    AS1 = nx.adjacency_spectrum(unfrozen_graph)
    m1 = np.real(AS1).round(2).max()
    da.append(float(format(abs(m-m1)/m,'.2f')))   #单独运算看对不对
    unfrozen_graph = nx.Graph(frozen_graph)
print(da.index(max(da)))#最大DA的节点
#print(nx.adjacency_matrix(unfrozen_graph).todense())#邻接矩阵矩阵形式 """

""" #degree_centrality
de_cen = nx.degree_centrality(G)
max_value,max_key = max(((v,k) for k,v in de_cen.items()))
print('degree centrality:',max_key)
#print(de_cen)
"""
""" #closeness_centrality
clo_cen = nx.closeness_centrality(G)
max_value,max_key = max(((v,k) for k,v in clo_cen.items()))
print(clo_cen)
print('closeness centrality:',max_key) """

"""
#eigenvector_centrality
eig_cen = nx.eigenvector_centrality(G)
max_value,max_key = max(((v,k) for k,v in eig_cen.items()))
print('eigenvector centrality:',max_key)
#print(eig_cen)
#betweenness_centrality
bet_cen = nx.betweenness_centrality(G)
max_value,max_key = max(((v,k) for k,v in bet_cen.items()))
print('betweenness centrality:',max_key)
#print(bet_cen)
#拉普拉斯算子的特征值
LS = nx.laplacian_spectrum(G)
print('拉普拉斯算子的特征值：\n',LS.round(2).max())#a.argmax()
AS = nx.adjacency_spectrum(G)
print('邻接矩阵的特征值：\n',AS.round(2).max()) """
#拉普拉斯算子的特征值
""" LS = nx.laplacian_spectrum(G)
print(LS)
print('拉普拉斯算子的特征值：\n',LS.round(2).argmax())#a.argmax() """


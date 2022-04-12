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


# N =5000#可以优化为不要每次都生成G，固定下来连接图
# # # #G = nx.scale_free_graph(N)
#BA=nx.random_graphs.barabasi_albert_graph(5000,5)   #BA无标度
""" BA=nx.random_graphs.barabasi_albert_graph(500,3)#(1000,3),2991条边 (400,3)1191边
print(len(BA.edges()))
# BA=nx.random_graphs.barabasi_albert_graph(200,3)
G = nx.Graph(BA) """
# print("len(nodes):",len(G.nodes()))
# print('len(edges):',len(G.edges()))
# #RG = nx.random_regular_graph(4,50)

""" WS = nx.watts_strogatz_graph(500,6,0.2)           #WS小世界，p可以改
print(len(WS.edges()))
G = WS
 """

""" B = np.load("BA500.npy")
G = nx.Graph(B)
# pos=nx.spring_layout(G)
# nx.draw(G,pos,node_size=1,with_labels = True)
# plt.show()
print("diameter:",nx.diameter(G))
degrees = dict(G.degree)
sum_of_edges = sum(degrees.values())/float(len(G))
print("ave degree",sum_of_edges)
print("len(nodes):",len(G.nodes()))
print('len(edges):',len(G.edges())) """
# print("ave degree:",nx.info(G))
#print("degree:",nx.degree(G))
#ER=nx.binomial_graph(5000,0.001)
# ER = nx.random_graphs.erdos_renyi_graph(5000,0.002)    #ER随机图
# print(len(ER.edges()))
# #SN=nx.powerlaw_cluster_graph(N,2,0.5)
# #B=np.load("unconnected.npy")#非完全连通子图
# G=BA
# G_center = nx.center(G)

""" fname = "anu214"
B = np.load(fname+".npy")#读取固定的图
G = nx.DiGraph(B)
print(nx.adjacency_matrix(G).todense())
#BA5000.npy是（5000,2）BA
# print('center:{}'.format(G_center))
print("G.edges()数量:",len(G.edges()))
#生成图的边的权重
with open(fname+"_weight.txt",'wt') as f:
    for u,v in G.edges():
        G.add_edge(u,v,weight=round(random.random(),2))
        #G.add_edge(v,u,weight=round(random.random(),2))
        print(u,v,G.get_edge_data(u,v)['weight'],file=f)
        #print(v,u,G.get_edge_data(v,u)['weight'],file=f) """
##print(G.edges())
# # p= dict(nx.shortest_path_length(G))
# # print('short_path:',p)
fname = "WS500"
B = np.load(fname+".npy")#读取固定的图
G = nx.DiGraph(B)
#BA5000.npy是(5000,2)BA
# print('center:{}'.format(G_center))
print("G.edges()数量:",len(G.edges()))
#生成图的边的权重
new_G = nx.DiGraph()
with open(fname+"_weight_2.txt",'wt') as f:
    for u,v in G.edges():
        new_G.add_edge(u,v,weight=round(random.random(),2))
        new_G.add_edge(v,u,weight=round(random.random(),2))
        print(u,v,new_G.get_edge_data(u,v)['weight'],file=f)
        print(v,u,new_G.get_edge_data(v,u)['weight'],file=f)
print(len(new_G.edges()))

'''
G = G = nx.complete_graph(N, nx.Graph())#全连接图
A=np.array(nx.adjacency_matrix(G).todense())#生成图的邻接矩阵
#print(A)
#pos=nx.spring_layout(G) 
#nx.draw(G,pos)
#nx.write_gexf(G,'28social_network_400000.gexf')
print('a')
#plt.show()
'''
#不用别人的算法，用networkx自带的算法
'''
G = nx.path_graph(30)#从30个节点单链开始
new_node=30
while new_node < N:
    
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
'''
# N = 100
# B = np.load("ws100_p.npy")#读取固定的图
# G = nx.Graph(B)

# adj_matrix = nx.adjacency_matrix(new_G).todense()
# print(adj_matrix)
# #G = nx.read_edgelist('./'+fname+'_weight.txt',nodetype = int,data=(('weight',float),),create_using=nx.Graph())
# pos=nx.spring_layout(G)
# # print(len(G.edges(data=True)))
# nx.draw(G,pos,node_size=1,with_labels = True)
# plt.show()
#print(nx.eccentricity(G))#G中所有节点的离心率
# print("半径：",nx.radius(G))#G的半径，离心率等于半径的点称为图的约旦中心（中心）
# print("直径：",nx.diameter(G))#图的直径，最短路径中最大的那个
# #nx.write_gexf(G,'28social_network_400000.gexf')

# A = nx.to_numpy_matrix(G) 
# np.save("./WS500",A)
# # print(A)
# print('a')


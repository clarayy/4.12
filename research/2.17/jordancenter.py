#部分观测且jordan center
#ob_B_SI.py+weight_jordancenter.py
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
from random import choice
import community as community_louvain
#变量：B，sn范围,每个sn张数 ，Infectionrate, Roundtime，data文件名
N =2068#记得必须改
fname = "p2p2068"
G = nx.read_edgelist('./'+fname+'_weight.txt',nodetype = int,data=(('weight',float),),create_using=nx.Graph())

part=0.5
Roundtime = 3

obn = int(N*0.5)  #有一半的节点可以观测到
observenode = random.sample(range(0,N-1),obn)#每次都随机选还是固定呢
#observenode= [i for i in range(62)]
print(obn,observenode)

#感染过程
node = list(map(int,G.nodes))#图中节点列表，元素转化为整数型
#node1 = list(set(node))#节点元素从小到大排序
#print(len(node))
S = node
I = []

j=0
while j<1:
    #start_node = random.choice(node)#1个初始感染节点
    start_node = 18#1个初始感染节点
    I.append(start_node)
    S.remove(start_node)
    j=j+1
print("start_node:")
print(start_node)
new_G = nx.Graph()    ###感染图
sub_new_G_b = nx.Graph()   ##观测到的感染图
sub_new_G_w = nx.Graph()   ##观测到的感染图
sub_new_G_m = nx.Graph() 
count = [1]
statechange = []
edgechange = []
edgeweight = []
weight_s = 1
#for i in range(Roundtime):
while len(I)<=part*len(G.nodes()):
    for nbr, datadict in G.adj.items():#遍历G的所有节点，nbr节点名称，datadict与节点相连的边
        if int(nbr) in S:
            node_adj = 0               #S节点的感染邻接点数
            for key in datadict:
                if int(key) in I:
                    node_adj=node_adj+1
                    edgechange.append(int(key))
                    edgeweight.append(G.get_edge_data(int(nbr),int(key))['weight'])
            for weight in edgeweight:
                weight_s = weight_s*(1-weight)
            rate = 1-weight_s
            if random.random() <= rate:   #被感染后，节点状态变化，感染图的边增加（周围所有感染节点与该点的连边都算上）
                # for a in edgechange:
                #     new_G.add_edge(int(nbr),a)
                statechange.append(int(nbr))
            edgechange = []
            edgeweight=[]
            weight_s=1            
    for i in statechange:
        S.remove(i)
        I.append(i)
    for nbr, datadict in G.adj.items():
        if int(nbr) in I:
            for key in datadict:
                if int(key) in I:
                    new_G.add_edge(int(nbr),int(key))
    for nbr, datadict in G.adj.items():
        if int(nbr) in I :
            if int(nbr) in observenode:
                for key in datadict:
                    if int(key) in I and int(key) in observenode:
                        sub_new_G_m.add_edge(int(nbr),int(key))
                        sub_new_G_b.add_edge(int(nbr),int(key),weight=G.edges[int(nbr),int(key)]['weight'])
                        sub_new_G_w.add_edge(int(nbr),int(key),weight=1-G.edges[int(nbr),int(key)]['weight'])
                    #elif int(key) not in observenode:

    if len(I)==1:
        break
    count.append(len(I))
    statechange = []

plt.figure()
Innum = plt.subplot(111)
props = {'title':'Total number of Infected Users',
          'ylabel':'number','xlabel':'time'}
Innum.set(**props)
x = []
for i in range(0,len(count)):
    x.append(i)
Innum.plot(x,count)
#Innum.text(0,0,'N:%.0f,Rate:%.4f' %(N,InfectionRate))
Innum.text(0,0,'N:%.0f' %N)
print("I=",I)
print('len(I):')
print(len(I))
plt.show()  #显示感染曲线

#nx.draw(new_G)
pos = nx.spring_layout(sub_new_G_m) #为什么报错！！！！！！！！！！
nx.draw(sub_new_G_m,pos,with_labels = True)#逗号是中文的  #画图
plt.show()

def jordancenter(G):
    lengths = nx.all_pairs_dijkstra_path_length(G,weight='weight')
    lengths = dict(lengths)
    ec = {}
    #for ei in range(len(lengths)):
    for ei in lengths:       #当观测图的编号不从0按顺序开始时；
        ec[ei]=max(lengths[ei].values())
    radius = min(ec.values())
    p = [v for v in ec if ec[v] == radius]
    return p

# center_frozen_graph = nx.freeze(sub_new_G_m)#G被冷冻为frozen_graph，不会改变
# center_unfrozen_graph = nx.Graph(center_frozen_graph)#删除节点在非冷冻图上进行，冷冻图不变
#Gc_node = max(nx.connected_components(sub_new_G_m), key=len)   #sub_newG的最大连通子图来求Jordan Center
#print(Gc_node)
# Gc = center_unfrozen_graph.subgraph(Gc_node)
# Jordan_center  = nx.center(Gc)
jc_b_all = []
for c in nx.connected_components(sub_new_G_b): #所有联通子图
    subgraph = sub_new_G_b.subgraph(c)
    x= jordancenter(subgraph)
    print("x:",x)
    jc_b_all.extend(x)

print("jc_b_all:",jc_b_all)
jc_w_all = []
for c in nx.connected_components(sub_new_G_w): #所有联通子图
    subgraph = sub_new_G_w.subgraph(c)
    x= jordancenter(subgraph)
    print("x:",x)
    jc_w_all.extend(x)

print("jc_w_all:",jc_w_all)
jc_m_all = []
for c in nx.connected_components(sub_new_G_m): #所有联通子图
    subgraph = sub_new_G_m.subgraph(c)
    x= jordancenter(subgraph)
    print("x:",x)
    jc_m_all.extend(x)

print("jc_m_all:",jc_m_all)

# jc_b = jordancenter(sub_new_G_b)
# jc_w = jordancenter(sub_new_G_w)
# jc_m = jordancenter(sub_new_G_m)
# print("jc_b:",jc_b)  #有可能是非完全联通的
# print("jc_w:",jc_w) 
# print("jc_m:",jc_m) 
read_dic = np.load(fname+"_short_path.npy",allow_pickle = True).item()
sumb=0
for i in range(len(jc_b_all)):
    a = read_dic[start_node][jc_b_all[i]]
    sumb = sumb+a
dis_b = sumb/len(jc_b_all)
sumw=0
for i in range(len(jc_w_all)):
    a = read_dic[start_node][jc_w_all[i]]
    sumw = sumw+a
dis_w = sumw/len(jc_w_all)
summ=0
for i in range(len(jc_m_all)):
    a = read_dic[start_node][jc_m_all[i]]
    summ = summ+a
dis_m = summ/len(jc_m_all)

print("dis_b:",dis_b)
print("dis_w:",dis_w)
print("dis_m:",dis_m)


jc_c_all = []
for c in nx.connected_components(sub_new_G_m): #所有联通子图
    subgraph = sub_new_G_m.subgraph(c)
    x= nx.center(subgraph)
    print("x:",x)
    jc_c_all.extend(x)
print("jc_c_all:",jc_c_all)
print("jc_c_all_dis:",read_dic[start_node][jc_c_all[0]])
#jc_sub_m = nx.center(sub_new_G_m)     #有可能是非完全连接图
#print("jc_sub_m:",jc_sub_m)
#print("jc_sub_m_dis:",read_dic[start_node][jc_sub_m[0]])


jc_inf = nx.center(new_G)
print("jc_inf:",jc_inf)
print("jc_inf_dis:",read_dic[start_node][jc_inf[0]])

#在一张图上显示
Gt=new_G.copy()
for node in I:
    if node!= start_node:
        Gt.remove_node(node)
#print(len(Gt.nodes()))#源节点
#print(len(G.nodes()))
pos = nx.spring_layout(G)
nx.draw(G,pos,node_color='b',node_size=1,edge_color = 'b',with_labels=True)
nx.draw_networkx_nodes(new_G,pos,node_color='r',node_size=1)
nx.draw_networkx_edges(new_G,pos,edge_color = 'r')
nx.draw_networkx_nodes(sub_new_G_b,pos,node_color='y',node_size=1)
nx.draw_networkx_edges(sub_new_G_b,pos,edge_color = 'y')
nx.draw(Gt,pos,node_color = 'g',node_size = 10)
plt.show()
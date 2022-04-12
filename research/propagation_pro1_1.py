#propagation使用的是从I开始遍历，使S改变状态
#本程序从S开始遍历，感染概率为1-（1-q）^n
#在一张图上同时显示初始图结构和传播感染图，即传播感染图是初始图结构的一部分
#可观测节点 图命名为observe
#propagation_pro1.py的扩展，多张图在一张图上显示，选择部分节点作为可观测节点

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
G = nx.Graph(B)    #20节点总图

#感染过程
node = list(map(int,G.nodes))#图中节点列表，元素转化为整数型
#node1 = list(set(node))#节点元素从小到大排序
#print(len(node))
S = node
I = []
observenode = random.sample(range(0,N-1),int(N*0.5))
print(observenode)
j=0
while j<1:
    #start_node = random.choice(node)#1个初始感染节点
    start_node = 2#1个初始感染节点
    I.append(start_node)
    S.remove(start_node)
    j=j+1
print("start_node:")
print(start_node)

new_G_small = nx.Graph()  #感染图
sub_newG = nx.Graph()   #可观测感染图
count = [1]
statechange = []
edgechange = []
InfectionRate = 0.5#概率太大，10轮感染1400个节点
Roundtime = 30
for i in range(Roundtime):
    for nbr, datadict in G.adj.items():#遍历G的所有节点，nbr节点名称，datadict与节点相连的边
        if int(nbr) in S:
            node_adj = 0               #S节点的感染邻接点数
            for key in datadict:
                if int(key) in I:
                    node_adj=node_adj+1
                    edgechange.append(int(key))
            rate = 1-(1-InfectionRate)**node_adj
            if random.random() <= rate:   #被感染后，节点状态变化，感染图的边增加（周围所有感染节点与该点的连边都算上）
                for a in edgechange:
                    new_G_small.add_edge(a,int(nbr))   #(I，S)感染节点在前
                    #if a in observenode and int(nbr) in observenode:    #情况A。只考虑这一个条件，得到的可能为非连通子图
                    #    sub_newG.add_edge(a,int(nbr))
                    #elif a not in observenode and int(nbr) in observenode: #情况C
                    #    sub_newG.add_edge(a,int(nbr))
                    if int(nbr) in observenode:    #情况A+C
                        sub_newG.add_edge(a,int(nbr))
                statechange.append(int(nbr))
            edgechange = []
    for i in statechange:
        S.remove(i)
        I.append(i)
    count.append(len(I))
    statechange = []
new_G = nx.Graph()  #可观测感染图，增加所有节点，在此基础上获得邻接矩阵
new_G.add_nodes_from(i for i in range(N))
new_G.add_edges_from(sub_newG.edges())
adj_matrix = nx.adjacency_matrix(new_G).todense()
print(adj_matrix)
plt.figure()
Innum = plt.subplot(111)
props = {'title':'Total number of Infected Users',
          'ylabel':'number','xlabel':'time'}
Innum.set(**props)
x = []
for i in range(0,len(count)):
    x.append(i)
Innum.plot(x,count)
Innum.text(0,0,'N:%.0f,Rate:%.4f' %(N,InfectionRate))
print('len(I):')
print(len(I))
plt.show()  #显示感染曲线

#显示源节点
#存储边数据
nx.write_edgelist(new_G_small,'new_G_small_edgelist.txt',delimiter=',',data = False)
nx.write_edgelist(new_G,'new_G_edgelist.txt',delimiter=',',data = False)
#print(new_G.edges())
#print(len(new_G.edges()))
print('len(new_G.nodes()):')
print(len(new_G.nodes()))
print('edges:')
print(new_G.edges())

#nx.draw(new_G)
pos = nx.spring_layout(new_G_small) #为什么报错！！！！！！！！！！
nx.draw(new_G_small,pos,with_labels = True)#逗号是中文的  #画图
plt.show()
nx.write_edgelist(sub_newG,'sub_newG_edgelist.txt',delimiter=',',data = False)
pos = nx.spring_layout(sub_newG) 
nx.draw(sub_newG,pos,with_labels = True)
plt.show()

Gc_node = max(nx.connected_components(sub_newG), key=len)   #sub_newG的最大连通子图来求Jordan Center
print(Gc_node)
Gc = sub_newG.subgraph(Gc_node)   #此时sub_newG改变，变为它自己的最大连通子图，也就是说此时Gc与sub_newG大小一样
pos = nx.spring_layout(Gc) 
nx.draw(Gc,pos,with_labels = True)
plt.show()
Jordan_center  = nx.center(Gc)
print("Jordan Center:",Jordan_center)    

#在一张图上显示
Gt=new_G_small.copy()
for node in I:
    if node!= start_node:
        Gt.remove_node(node)
#print(len(Gt.nodes()))#源节点
#print(len(G.nodes()))
pos1 = nx.spring_layout(G)
nx.draw(G,pos1,node_color='b',node_size=1,edge_color = 'b')
nx.draw_networkx_nodes(new_G_small,pos1,node_color='r',node_size=1)  #感染图
nx.draw_networkx_edges(new_G_small,pos1,edge_color = 'r')
#nx.draw_networkx_nodes(sub_newG,pos1,node_color='y',node_size=1)    #可观测图, sub_newG与Gc画出来一样。
#nx.draw_networkx_edges(sub_newG,pos1,edge_color = 'y')
nx.draw(new_G,pos1,node_color='b',node_size=1,edge_color = 'y')       #可观测图
nx.draw(Gc,pos1,node_color='w',node_size=1,edge_color = 'w')          #Jordan Center
nx.draw(Gt,pos1,node_color = 'green',node_size = 10)   #感染源
plt.show()

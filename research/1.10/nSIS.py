#根据感染节点得到传播图
##考虑权重的SIS ，边的权重，节点的属性
#SIS模型中的恢复率考虑两种情况：1.每个节点的恢复率不同2.恢复率统一
#SIS模型
#感染概率0.5，恢复概率0.1
#propagation使用的是从I开始遍历，使S改变状态
#本程序从S开始遍历，感染概率为1-（1-q）^n
#在一张图上同时显示初始图结构和传播感染图，即传播感染图是初始图结构的一部分
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import networkx as nx
import os
import random
from itertools import islice
import math

N =500
fname = "food500"
# InfectionRate = 0.5#概率太大，10轮感染1400个节点
part = 0.1
ReturnRate = 0.5 #再次成为S状态
Roundtime = 30  #5轮往后开始波动，因此取4
G = nx.read_edgelist('./'+fname+'_weight.txt',nodetype = int,data=(('weight',float),),create_using=nx.Graph())
#attrs = np.load(fname+'_node_attrs.npy',allow_pickle = 'TRUE')
#nx.set_node_attributes(G,attrs.item())
#感染过程
node = list(map(int,G.nodes))#图中节点列表，元素转化为整数型
#node1 = list(set(node))#节点元素从小到大排序
#print(len(node))
S = node
I = []

j=0
while j<1:
    #start_node = random.choice(node)#1个初始感染节点
    start_node = 0#1个初始感染节点
    I.append(start_node)
    S.remove(start_node)
    j=j+1
print("start_node:",start_node)

new_G = nx.Graph()
new_G.add_node(start_node)
count = [1]
countS = [N-1]
statechange = []
statechange1 = []
edgechange = []
edgeweight = []
weight_s = 1
#for i in range(Roundtime):
while len(I)<=part*len(G.nodes()):
    for nbr, datadict in G.adj.items():#遍历G的所有节点，nbr节点名称，datadict与节点相连的边
        if int(nbr) in S:
            node_adj = 0               #S节点的感染邻接点数
            for key in datadict:
                #if int(key) in I and int(key) not in statechange1: #降低了S节点受感染的概率
                if int(key) in I:   #增加了72，73行
                    node_adj=node_adj+1
                    edgechange.append(int(key))
                    edgeweight.append(G.get_edge_data(int(nbr),int(key))['weight'])
            for weight in edgeweight:
                weight_s = weight_s*(1-weight)
            rate = 1-weight_s
            if random.random() <= rate:   #被感染后，节点状态变化，感染图的边增加（周围所有感染节点与该点的连边都算上）
                # for a in edgechange:
                #     new_G.add_edge(a,int(nbr))
                statechange.append(int(nbr))
            edgechange = []
            edgeweight=[]
            weight_s=1 
        if int(nbr) in I and int(nbr)!=start_node:
            if random.random() <=ReturnRate:
            #if random.random() <=G.nodes[int(nbr)]['recover']: 
                statechange1.append(int(nbr))
                #new_G.remove_node(int(nbr))
    for i in statechange:
        S.remove(i)
        I.append(i)
    for i in statechange1:
        I.remove(i)
        S.append(i)
        # if i in new_G.nodes():
        #     new_G.remove_node(i)
    print("I=",I)
    new_G =nx.Graph()
    for nbr, datadict in G.adj.items():
        if int(nbr) in I:
            for key in datadict:                
                if int(key) in I:
                    new_G.add_edge(int(nbr),int(key))    
    # print("new_G.nodes()",new_G.nodes())
    # print("new_G.egdes()",new_G.edges())
    #print("new_G_y.egdes()",new_G_y.edges())
    count.append(len(I))
    countS.append(len(S))
    statechange = []
    statechange1 = []
print("len(new_G nodes):",len(new_G.nodes()))
center_frozen_graph = nx.freeze(new_G)#G被冷冻为frozen_graph，不会改变
center_unfrozen_graph = nx.Graph(center_frozen_graph)#删除节点在非冷冻图上进行，冷冻图不变
every_jc = []
for c in nx.connected_components(new_G): #所有联通子图
    nodeSet = new_G.subgraph(c).nodes()
    subgraph = new_G.subgraph(c)
    #plt.subplot(subplot[0])
    Jordan_center  = nx.center(subgraph)
    print("jc:",Jordan_center)
    nx.draw_networkx(subgraph,with_labels=True)
    print("len(nodes):",len(subgraph.nodes()))
    plt.show()
    every_jc.extend(Jordan_center)
print("every_jc:",every_jc)
Gc_node = max(nx.connected_components(new_G), key=len)   #sub_newG的最大连通子图来求Jordan Center
#print(Gc_node)
Gc = center_unfrozen_graph.subgraph(Gc_node)    #改变了new_G_small，使其成为最大连通子图
Jordan_center  = nx.center(Gc)
print("jc:",Jordan_center)
print("len(new_G nodes):",len(new_G.nodes()))
#无偏中介中心性
bet_cen = nx.betweenness_centrality(new_G)#节点的中介中心性
deg = new_G.degree()#节点的度
ub={}
for i in bet_cen.keys():
    if deg[i]!=0:
        ub[i] = bet_cen[i]/(math.pow(deg[i],0.85))
unbiased_betweenness = max(ub, key=lambda x: ub[x])
print("ub:",unbiased_betweenness)

#distance centrality
p = dict(nx.shortest_path_length(new_G))
d={}
for k,v in p.items():
    s=0
    for i in v.values():
        s = s+i
    d[k] = s
distance_centrality = min(d, key=lambda x: d[x])
print("dc:",distance_centrality)
#dynamic ages
frozen_graph = nx.freeze(new_G)#G被冷冻为frozen_graph，不会改变
unfrozen_graph = nx.Graph(frozen_graph)#删除节点在非冷冻图上进行，冷冻图不变
AS = nx.adjacency_spectrum(frozen_graph)#邻接矩阵特征值
m = np.real(AS).round(4).max()
all_nodes = new_G.nodes
#print(all_nodes)
da = {}                             ###!!!!!字典才对
for i in all_nodes:
    unfrozen_graph.remove_node(i)
    AS1 = nx.adjacency_spectrum(unfrozen_graph)
    m1 = np.real(AS1).round(4).max()
    da[i] = float(format(abs(m-m1)/m,'.4f'))   #单独运算看对不对
    unfrozen_graph = nx.Graph(frozen_graph)
dynage = max(da, key=lambda x: da[x])
print("da:",dynage)

plt.figure()
Innum = plt.subplot(111)
props = {'title':'Total number of Infected Users',
          'ylabel':'number','xlabel':'time'}
Innum.set(**props)
x = []
for i in range(0,len(count)):
    x.append(i)
Innum.plot(x,count,'r-',label ='I')
Innum.plot(x,countS,'b-',label ='S')
#Innum.text(0,0,'N:%.0f,Rate:%.4f' %(N,InfectionRate))

print('len(S):',len(S))
print('len(I):',len(I))
plt.legend()
plt.show()  #显示感染曲线

#显示源节点
#存储边数据
#nx.write_edgelist(new_G,'data_G1.txt',delimiter=',',data = False)
#print(new_G.edges())
#print(len(new_G.edges()))
# print('len(new_G.nodes()):')
# print(len(new_G.nodes()))
# print('edges:')
# print(new_G.edges())
print('len(edges):',len(new_G.edges()))
print("I:",I)
print("new_G.nodes():",new_G.nodes())
#nx.draw(new_G)
pos = nx.spring_layout(new_G) #为什么报错！！！！！！！！！！
nx.draw(new_G,pos,with_labels = True)#逗号是中文的  #画图
plt.show()

#在一张图上显示
Gt=new_G.copy()

for node in new_G.nodes():
    if node!= start_node:
        Gt.remove_node(node)
print("Gt.nodes():",Gt.nodes())
#print(len(Gt.nodes()))#源节点
#print(len(G.nodes()))
pos = nx.spring_layout(G)
nx.draw(G,pos,node_color='b',node_size=1,edge_color = 'b',with_labels=True)
nx.draw_networkx_nodes(new_G,pos,node_color='y',node_size=1)
nx.draw_networkx_edges(new_G,pos,edge_color = 'y')
# nx.draw_networkx_nodes(new_G_y,pos,node_color='r',node_size=1)  #比较大
# nx.draw_networkx_edges(new_G_y,pos,edge_color = 'r')
nx.draw(Gt,pos,node_color = 'green',node_size = 10)
plt.show()

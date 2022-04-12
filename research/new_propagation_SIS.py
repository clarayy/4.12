#SIS模型
#propagation使用的是从I开始遍历，使S改变状态
#本程序从I开始遍历，感染概率为Infectionrate
#在一张图上同时显示初始图结构和传播感染图，即传播感染图是初始图结构的一部分
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import networkx as nx
import os
import random
from itertools import islice


N = 20
B = np.load("BA20.npy")#读取固定的图
G = nx.Graph(B)

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
print("start_node:")
print(start_node)

new_G = nx.Graph()
new_G.add_node(start_node)
count = [1]
countS = [N-1]
StoI = []
ItoS = []
edgechange = []
InfectionRate = 0.3#概率太大，10轮感染1400个节点
ReturnRate = 0.4 #再次成为S状态
Roundtime = 5
for i in range(Roundtime):
    for nbr, datadict in G.adj.items():#遍历G的所有节点，nbr节点名称，datadict与节点相连的边
        if int(nbr) in I:              #I节点的感染邻接点数
            for key in datadict:
                if int(key) in S:
                    if random.random() <= InfectionRate:
                        StoI.append(int(key))
                        new_G.add_edge(int(nbr),int(key)) #(I,S)
            if random.random() <= ReturnRate and int(nbr)!= start_node: #同一时间轮时，先感染后恢复成S，独立吗？？
                ItoS.append(int(nbr))
                new_G.remove_node(int(nbr))
    set_statechange=list(set(StoI))
    for i in set_statechange:
        I.append(i)
        if i in S:
            S.remove(i)
    for i in ItoS:
        I.remove(i)
        S.append(i)
    count.append(len(I))
    countS.append(len(S))
    StoI = []
    ItoS = []
    


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
Innum.text(0,0,'N:%.0f,Rate:%.4f' %(N,InfectionRate))
print('len(I):')
print(len(I))
plt.legend()
plt.show()  #显示感染曲线

#显示源节点
#存储边数据
#nx.write_edgelist(new_G,'data_G1.txt',delimiter=',',data = False)
#print(new_G.edges())
#print(len(new_G.edges()))
print('len(new_G.nodes()):')
print(len(new_G.nodes()))
print('edges:')
print(new_G.edges())

print("I:",list(set(I)))
print(list(set(new_G.nodes())))
#nx.draw(new_G)
pos = nx.spring_layout(new_G) #为什么报错！！！！！！！！！！
nx.draw(new_G,pos,with_labels = True)#逗号是中文的  #画图
plt.show()

#在一张图上显示
Gt=new_G.copy()
for node in I:
    if node!= start_node:
        Gt.remove_node(node)
print(Gt.nodes())
#print(len(Gt.nodes()))#源节点
#print(len(G.nodes()))
pos = nx.spring_layout(G)
nx.draw(G,pos,node_color='b',node_size=1,edge_color = 'b')
nx.draw_networkx_nodes(new_G,pos,node_color='r',node_size=1)
nx.draw_networkx_edges(new_G,pos,edge_color = 'r')
nx.draw(Gt,pos,node_color = 'green',node_size = 10)
plt.show()

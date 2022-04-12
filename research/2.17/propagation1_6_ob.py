#给感染节点一个label， 感染状态作为node_labels
#部分观测
#新的感染图画法，添加边根据所有感染节点来增加
#propagation_pro1.py的升级
#给边增加权重，随机增加
#改为传播到总结点数的0.8停止传播
#propagation使用的是从I开始遍历，使S改变状态
#本程序从S开始遍历，感染概率为1-（1-q）^n
#在一张图上同时显示初始图结构和传播感染图，即传播感染图是初始图结构的一部分
#from research.new_propagation_SI import InfectionRate, Roundtime
from cProfile import label
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import networkx as nx
import os
import random
from itertools import islice
import argparse
from scipy.sparse.coo import coo_matrix
from sklearn.semi_supervised import LabelSpreading

N =62
name = "dolphins"
B = np.load(name+".npy")#读取固定的图
G = nx.Graph(B)
# adj_matrix = nx.adjacency_matrix(G).todense()
# coo_A=coo_matrix(adj_matrix)   #邻接矩阵的边的行/列的坐标
# edge_index = [coo_A.row+1,coo_A.col+1]
# print(len(edge_index))
G = nx.read_edgelist('./'+name+'_weight.txt',nodetype = int,data=(('weight',float),),create_using=nx.Graph())
print(len(G.edges()))

obn = int(N*0.5)  #有一半的节点可以观测到
#observenode = random.sample(range(0,N-1),obn)#每次都随机选还是固定呢
#observenode= [i for i in range(62)]
observenode=[21, 38, 27, 42, 55, 16, 58, 60, 28, 49, 26, 51, 45, 17, 11, 33, 41, 57, 39, 10, 18, 34, 25, 36, 20, 53, 56, 23, 3, 24, 52]#62,0.5
print(obn,observenode)

InfectionRate = 0.1#概率太大，10轮感染1400个节点
Roundtime =3
part = 0.1

#感染过程
node = list(map(int,G.nodes))#图中节点列表，元素转化为整数型
#node1 = list(set(node))#节点元素从小到大排序
#print(len(node))
S = node
I = []

j=0
while j<1:
    #start_node = random.choice(node)#1个初始感染节点
    start_node =25#1个初始感染节点
    I.append(start_node)
    S.remove(start_node)
    j=j+1
print("start_node:")
print(start_node)

new_G = nx.Graph()
ob_G = nx.Graph()
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
    if len(I)==1:
        break
    count.append(len(I))
    statechange = []
for nbr, datadict in G.adj.items():
    if int(nbr) in observenode:
        for key in datadict:
            if int(key) in observenode:
                ob_G.add_edge(int(nbr),int(key))
# pos = nx.spring_layout(ob_G) #为什么报错！！！！！！！！！！
# nx.draw(ob_G,pos,with_labels = True)#逗号是中文的  #画图
# plt.show()
# print(ob_G.nodes())
G_x =[]#62节点中属于I且属于ob状态的节点
for i in range(N):
    if i in I:
        if i in ob_G.nodes():
            G_x.append(i)
print("G_x:",G_x)
relabel_ob_G = nx.Graph()
mapping={}
relabel_ob_G_x={}
it=0
for n in ob_G.nodes():
    mapping[n]=it
    if n in I:
        relabel_ob_G_x[it]=2
    else:
        relabel_ob_G_x[it]=1
    it+=1
# indexed from 0
print("relabel_ob_G_x:",relabel_ob_G_x)  #26个观测节点的状态S/I
relabel_ob_G=nx.relabel_nodes(ob_G, mapping)     #此时两种图的节点命名应该是不同的
adj_matrix = nx.adjacency_matrix(ob_G).todense()
adj_matrix_relabel = nx.adjacency_matrix(relabel_ob_G).todense()
print(adj_matrix)
print(adj_matrix_relabel.all()==adj_matrix.all())
coo_A=coo_matrix(adj_matrix)   #邻接矩阵的边的行/列的坐标
coo_A_relabel = coo_matrix(adj_matrix_relabel)      #看两种图得到的coo是否是相同的
edge_index = [coo_A.row+1,coo_A.col+1]
edge_index_label = [coo_A_relabel.row+1,coo_A_relabel.col+1]
print(edge_index)
print(edge_index_label)
print(len(edge_index[0]))
def adjConcat(a, b):
    '''
    将a,b两个矩阵沿对角线方向斜着合并，空余处补零[a,0.0,b]
    得到a和b的维度，先将a和b*a的零矩阵按行（竖着）合并得到c，再将a*b的零矩阵和b按行合并得到d
    将c和d横向合并
    '''
    lena = len(a)
    lenb = len(b)
    left = np.row_stack((a, np.zeros((lenb, lena),dtype=int)))  # 先将a和一个len(b)*len(a)的零矩阵垂直拼接，得到左半边
    right = np.row_stack((np.zeros((lena, lenb),dtype=int), b))  # 再将一个len(a)*len(b)的零矩阵和b垂直拼接，得到右半边
    result = np.hstack((left, right))  # 将左右矩阵水平拼接
    return result
island = len(observenode)-len(ob_G.nodes())
adj_new = adjConcat(adj_matrix,np.zeros((island,island),dtype=int))
print(adj_new)
g_n_i=len(relabel_ob_G_x)
for g_n in observenode:
    if g_n not in ob_G.nodes():
        if g_n in I:
            relabel_ob_G_x[g_n_i]=2
        else:
            relabel_ob_G_x[g_n_i]=1
        g_n_i +=1
print("relabel_ob_G_x:",relabel_ob_G_x)
# resultall={}
# for i in range(N):
#     if i in I:
#         resultall[i]=2
#     else:
#         resultall[i]=1
# print(resultall)
#print(G.edges())
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
print('len(I):',len(I))
print("I=",I)
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

#nx.draw(new_G)
pos = nx.spring_layout(new_G) #为什么报错！！！！！！！！！！
nx.draw(new_G,pos,with_labels = True)#逗号是中文的  #画图
plt.show()

#在一张图上显示
Gt=new_G.copy()
for node in I:
    if node!= start_node:
        Gt.remove_node(node)
#print(len(Gt.nodes()))#源节点
#print(len(G.nodes()))
pos = nx.spring_layout(G)
print("len(G.edges():",len(G.edges()))
nx.draw(G,pos,node_color='b',node_size=1,edge_color = 'b',with_labels=True)
nx.draw_networkx_nodes(observenode,pos,node_color='r',node_size=5)
nx.draw_networkx_nodes(I,pos,node_color='g',node_size=15)
nx.draw_networkx_edges(ob_G,pos,edge_color = 'r')
nx.draw(Gt,pos,node_color = 'red',node_size = 10,with_labels=True)
plt.show()

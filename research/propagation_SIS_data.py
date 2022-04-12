#SIS模型
#生成多张图的数据
#生成每个子图的无偏中介中心性，距离中心性，动态年龄属性

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
#变量：B，sn范围,每个sn张数 ，Infectionrate, Roundtime，data文件名

N = 62
fname = "dolphins"
B = np.load(fname+".npy")#读取固定的图
G = nx.Graph(B)

countedge = []
countadj = []

graph_labels = []
InfectionRate = 0.5#概率太大，10轮感染1400个节点
ReturnRate = 0.3 #再次成为S状态
Roundtime = 6
def genGraph(sn,datadir,bmname):

#感染过程
    node = list(map(int,G.nodes))#图中节点列表，元素转化为整数型
    S = node
    I = []
    j=0
    while j<1:
        #start_node = random.choice(node)#1个初始感染节点
        start_node = sn#1个初始感染节点
        I.append(start_node)
        S.remove(start_node)
        j=j+1
    
    print(start_node)
    
    new_G_small = nx.Graph()
    new_G_small.add_node(sn)
    count = [1]
    countS = [N-1]
    statechange = []
    statechange1 = []
    edgechange = []

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
                        new_G_small.add_edge(a,int(nbr))
                    statechange.append(int(nbr))
                edgechange = []
            if int(nbr) in I and int(nbr)!=start_node:
                #if Roundtime>1:  #假设一段时间以后感染节点才开始进行恢复
                if random.random() <=ReturnRate:
                    statechange1.append(int(nbr))
                    new_G_small.remove_node(int(nbr))
        for i in statechange:
            S.remove(i)
            I.append(i)
        for i in statechange1:
            I.remove(i)
            S.append(i)
            if i in new_G_small.nodes():
                new_G_small.remove_node(i)
        #if nx.is_empty(new_G_small):
        #    break
        count.append(len(I))
        countS.append(len(S))
        statechange = []
        statechange1 = []
    perfix = os.path.join(datadir,bmname)
    filename_node_labels = perfix + '_node_labels.txt'
    filename_center = perfix + '_jordancenter.txt'
    filename_center1 = perfix + '_jordancenter1.txt'
    filename_unbet = perfix + '_unbet.txt'
    filename_discen = perfix + '_discen.txt'
    filename_dynage = perfix + '_dynage.txt'
    #new_G_small表示感染图
    #new_G表示感染图加上未感染的节点，
    #将new_G中的邻接矩阵扩展到G
    new_G = nx.Graph()
    new_G.add_nodes_from(i for i in range(N))
    new_G.add_edges_from(new_G_small.edges())
    #Jordan_center  = nx.center(new_G)#非全连接图不能计算
    # print(new_G.nodes())
    # nx.draw(new_G_small,with_labels =True)
    # plt.show()
    if not nx.is_empty(new_G):
        adj_matrix = nx.adjacency_matrix(new_G).todense()
        #Jordan center
        center_frozen_graph = nx.freeze(new_G_small)#G被冷冻为frozen_graph，不会改变
        center_unfrozen_graph = nx.Graph(center_frozen_graph)#删除节点在非冷冻图上进行，冷冻图不变
        Gc_node = max(nx.connected_components(new_G_small), key=len)   #sub_newG的最大连通子图来求Jordan Center
        #print(Gc_node)
        Gc = center_unfrozen_graph.subgraph(Gc_node)    #改变了new_G_small，使其成为最大连通子图
        Jordan_center  = nx.center(Gc)
        #print("jc:",Jordan_center)
        with open(filename_center,'a') as centerf:
            centerf.write(str(choice(Jordan_center)))    #Jordan center随机选，按理来说差别可能不大，实际有差别
            centerf.write('\n')
        with open(filename_center1,'a') as centerf1:
            centerf1.write(str(Jordan_center[0]))    #Jordan center选第一个
            centerf1.write('\n')
        #无偏中介中心性
        bet_cen = nx.betweenness_centrality(new_G_small)#节点的中介中心性
        deg = new_G_small.degree()#节点的度
        ub={}
        for i in bet_cen.keys():
            if deg[i]!=0:
                ub[i] = bet_cen[i]/(math.pow(deg[i],0.85))
        #print(deg)
        #print(ub)
        unbiased_betweenness = max(ub, key=lambda x: ub[x])
        #unbiased_betweenness = ub.index(max(ub))#####list中index不是对应的节点编号，因为节点编号不是连续的。还得用字典
        with open(filename_unbet,'a') as unbetf:
            unbetf.write(str(unbiased_betweenness))
            unbetf.write('\n')

        #distance centrality
        p = dict(nx.shortest_path_length(new_G_small))
        d={}
        for k,v in p.items():
            s=0
            for i in v.values():
                s = s+i
            d[k] = s
        distance_centrality = min(d, key=lambda x: d[x])
        with open(filename_discen,'a') as discenf:
            discenf.write(str(distance_centrality))
            discenf.write('\n')

        #dynamic ages
        frozen_graph = nx.freeze(new_G_small)#G被冷冻为frozen_graph，不会改变
        unfrozen_graph = nx.Graph(frozen_graph)#删除节点在非冷冻图上进行，冷冻图不变
        AS = nx.adjacency_spectrum(frozen_graph)#邻接矩阵特征值
        m = np.real(AS).round(4).max()
        all_nodes = new_G_small.nodes
        #print(all_nodes)
        da = {}                             ###!!!!!字典才对
        for i in all_nodes:
            unfrozen_graph.remove_node(i)
            AS1 = nx.adjacency_spectrum(unfrozen_graph)
            m1 = np.real(AS1).round(4).max()
            da[i] = float(format(abs(m-m1)/m,'.4f'))   #单独运算看对不对
            unfrozen_graph = nx.Graph(frozen_graph)
        dynage = max(da, key=lambda x: da[x])
        with open(filename_dynage,'a') as dynagef:
            dynagef.write(str(dynage))
            dynagef.write('\n')
        # print("jc:",Jordan_center)
        # print("ub:",unbiased_betweenness)
        # print("shortpath:",p)
        # print("dc:",distance_centrality)
        # print("dn:",dynage)
    #np.savetxt('datatest.txt',adj_matrix)
    #print(adj_matrix.shape)
        countadj_now=adj_matrix.shape[1]
        countadj.append(adj_matrix.shape[1])
        countedge.append(new_G.number_of_edges())
        with open(filename_node_labels,'a') as labelf:#节点ID作为标签
            for i in new_G.nodes:
                labelf.write(str(i))
                labelf.write('\n')
        graph_labels.append(start_node)

    else:
        adj_matrix=[]
        countadj_now=[]
    
    return (adj_matrix,countadj_now)

#可以自己造邻接矩阵，行和列的范围从adj_matrix.shape开始增加
#直接生成data_A.txt  边的邻接矩阵
def data_A(datadir,bmname):
    perfix = os.path.join(datadir,bmname)
    filename_A = perfix + '_A.txt'
    filename_node_labels = perfix + '_dre_node_labels.txt'
    sum_ca_now = 0
    graphs=100
    nodehead=0
    nodetail=N
    #nodelist = [0,2,4,18,9,35,8,41]   #BA100.npy的分类 8类
    #nodelist = [9,2,5,0,15,6,14,31]    #rg_4_100的分类 8类
    #nodelist = [0,1,2,8,10,37,65,11]    #ws_smallworld 8类
    with open(filename_A,'w') as f:
        with open(filename_node_labels,'w') as f1: #节点度记录
            #for nodesn in nodelist:
            for nodesn in range(nodehead,nodetail):
                for j in range(graphs):
                    adj,ca_now=genGraph(nodesn,datadir,bmname)
                    if len(adj):                      #图为非空，才进行下一步
                        coo_A=coo_matrix(adj)   #邻接矩阵的边的行/列的坐标
                        edge_index = [coo_A.row,coo_A.col]
                        #node_labels(adj)
                        a=np.array(adj)
                        a=np.sum(a,axis=1)
                        a=a.tolist()
                        for i in range(len(a)):
                            f1.write(str(a[i]))
                            f1.write('\n')
                        if len(countadj)==1:
                            for i in range(len(edge_index[1])):
                                f.write(str(coo_A.row[i])+','+str(coo_A.col[i]))
                                f.write('\n')
                                #print(str(coo_A.row[i])+','+str(coo_A.col[i]))
                        else:
                            for i in range(len(edge_index[1])):
                                f.write(str(coo_A.row[i]+sum_ca_now)+','+str(coo_A.col[i]+sum_ca_now))
                                f.write('\n')
                                #print(str(coo_A.row[i]+sum_ca_now)+','+str(coo_A.col[i]+sum_ca_now))
                        sum_ca_now=sum_ca_now+ca_now
    #/home/zhang/Documents/pytorch/learn/GraphKernel/rexying_diffpool/diffpool-master/data
    filename_readme = perfix + 'readme.txt'
    with open(filename_readme,'a') as f:
        f.write('InfectionRate='+str(InfectionRate)+"\n")
        f.write('ReturnRate='+str(ReturnRate)+"\n")
        f.write('Roundtime='+str(Roundtime)+"\n")
        f.write('[a,b]='+str(nodehead)+','+str(nodetail)+"\n")
        f.write('every node graphs='+str(graphs)+"\n")


def main():

    bmname = 'dolphins_SIS_g0.5_r6'
    path = os.path.join('/home/zhang/Documents/pytorch/learn/GraphKernel/rexying_diffpool/diffpool-master/data',bmname)
    #path = os.path.join('data',bmname)#调试时生成的文件夹
    if not os.path.exists(path):
        os.makedirs(path)
    perfix = os.path.join(path,bmname)
    filename_readme = perfix+'readme.txt'
    with open(filename_readme,'w') as f:
        f.write('bmname = '+str(bmname)+"\n")
        f.write('N='+str(N)+"\n")
        f.write('底图='+fname+".npy"+"\n")

    data=open(filename_readme,'a')
    data_A(path,bmname)
    graph_label(path,bmname)
    graph_indicator(path,bmname)

    s=0
    for i in countedge:
        s=s+i
    print('sum of edges:',file=data)
    print(str(s)+'\n',file=data)
    s1=0
    for i in countadj:
        s1=s1+i
    print('sum of adj:',file=data)
    print(str(s1)+'\n',file=data)

def graph_indicator(datadir,bmname):
    perfix = os.path.join(datadir,bmname)
    filename_graph_indic = perfix + '_graph_indicator.txt'
    with open(filename_graph_indic,'w') as f:
        i=1
        for val in countadj:
            for j in range(int(val)):
                f.write(str(i))
                f.write('\n')
            i=i+1
def graph_label(datadir,bmname):
    perfix = os.path.join(datadir,bmname)
    filename_graph_labels = perfix+ '_graph_labels.txt'
    with open(filename_graph_labels,'w') as f:
        for i in graph_labels:
            f.write(str(i))
            f.write('\n')

if __name__ == "__main__":
    main()

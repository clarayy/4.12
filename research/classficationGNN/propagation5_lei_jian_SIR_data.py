#propagation5_lei_jian的升级
#考虑边的权重且按照总数来生成传播图

#500节点时，如果同时计算其他方法的每张图的中心，很慢
#本程序将其他方法的计算分割开，不是不计算，而是直接写入简单的1，否则GNN也得改
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

N = 171
fname = "trap171"
# B = np.load(fname+".npy")#读取固定的图
# G = nx.Graph(B)
#RecoverRate = 0.4 #成为R状态
Roundtime = 4
G = nx.read_edgelist('./'+fname+'_weight.txt',nodetype = int,data=(('weight',float),),create_using=nx.Graph())
attrs = np.load(fname+'_node_attrs.npy',allow_pickle = 'TRUE')
nx.set_node_attributes(G,attrs.item())
#partition = community_louvain.best_partition(G)
#np.save("BA500_partition.npy",partition)
partition=np.load(fname+'_p'+'.npy',allow_pickle = True).item()
graph_labels = []
graph_labels_class=[]
countedge = []
countadj = []

# InfectionRate = 0.5#概率太大，10轮感染1400个节点
# Roundtime = 3
def genGraph(sn,datadir,bmname):

#感染过程
    node = list(map(int,G.nodes))#图中节点列表，元素转化为整数型
    S = node
    I = []
    R = []
    j=0
    while j<1:
        #start_node = random.choice(node)#1个初始感染节点
        start_node = sn#1个初始感染节点
        I.append(start_node)
        S.remove(start_node)
        j=j+1
    
    print(start_node)
    part = 0.4
    new_G_small = nx.Graph()
    new_G_small.add_node(sn)
    count = [1]
    countS = [N-1]
    countR = [0]
    statechange = []
    statechange1 = []
    edgechange = []
    edgeweight = []
    weight_s = 1
    for i in range(Roundtime):     #SIR模型用节点数可能会陷入死循环，所以用轮数
    #while len(I)<=part*len(G.nodes()):
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
                    for a in edgechange:
                        new_G_small.add_edge(int(nbr),a)
                    statechange.append(int(nbr))
                edgechange = []
                edgeweight=[]
                weight_s=1 
            if int(nbr) in I and int(nbr)!=start_node:     #固定恢复率的情况下
                #if random.random() <=RecoverRate:  
                #print(G.nodes[int(nbr)]['recover'])
                if random.random() <=G.nodes[int(nbr)]['recover']:              
                    statechange1.append(int(nbr))
                    new_G_small.remove_node(int(nbr))
        for i in statechange:
            S.remove(i)
            I.append(i)
        for i in statechange1:
            I.remove(i)
            R.append(i)
            if i in new_G_small.nodes():
                new_G_small.remove_node(i)
        count.append(len(I))
        countS.append(len(S))
        countR.append(len(R))
        statechange = []
        statechange1 = []
    perfix = os.path.join(datadir,bmname)
    filename_node_labels = perfix + '_node_labels.txt'
    filename_center = perfix + '_jordancenter.txt'
    filename_center1 = perfix + '_jordancenter1.txt'
    # filename_unbet = perfix + '_unbet.txt'
    # filename_discen = perfix + '_discen.txt'
    # filename_dynage = perfix + '_dynage.txt'
    #new_G_small表示感染图
    #new_G表示感染图加上未感染的节点，
    #将new_G中的邻接矩阵扩展到G
    new_G = nx.Graph()
    new_G.add_nodes_from(i for i in range(N))
    new_G.add_edges_from(new_G_small.edges())
    #Jordan_center  = nx.center(new_G)#非全连接图不能计算

    if not nx.is_empty(new_G):
        adj_matrix = nx.adjacency_matrix(new_G).todense()
        center_frozen_graph = nx.freeze(new_G_small)#G被冷冻为frozen_graph，不会改变
        center_unfrozen_graph = nx.Graph(center_frozen_graph)#删除节点在非冷冻图上进行，冷冻图不变
        Gc_node = max(nx.connected_components(new_G_small), key=len)   #sub_newG的最大连通子图来求Jordan Center
        #print(Gc_node)
        Gc = center_unfrozen_graph.subgraph(Gc_node)
        Jordan_center  = nx.center(Gc)
        #无偏中介中心性
        """ bet_cen = nx.betweenness_centrality(new_G_small)#节点的中介中心性
        deg = new_G_small.degree()#节点的度
        ub={}
        for i in bet_cen.keys():
            ub[i] = bet_cen[i]/(math.pow(deg[i],0.85))
        unbiased_betweenness = max(ub, key=lambda x: ub[x]) """
        #unbiased_betweenness = ub.index(max(ub))#####list中index不是对应的节点编号，因为节点编号不是连续的。还得用字典
        # unbiased_betweenness = 1
        # with open(filename_unbet,'a') as unbetf:
        #     unbetf.write(str(unbiased_betweenness))
        #     unbetf.write('\n')

        #distance centrality
        """ dis_path = dict(nx.shortest_path_length(new_G_small))
        dis_d={}
        for k,v in dis_path.items():
            dis_s=0
            for i in v.values():
                dis_s = dis_s+i
            dis_d[k] = dis_s
        distance_centrality = min(dis_d, key=lambda x: dis_d[x]) """
        # distance_centrality =1
        # with open(filename_discen,'a') as discenf:
        #     discenf.write(str(distance_centrality))
        #     discenf.write('\n')

        #dynamic ages
        """ frozen_graph = nx.freeze(new_G_small)#G被冷冻为frozen_graph，不会改变
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
        dynage = max(da, key=lambda x: da[x]) """
        # dynage=1
        # with open(filename_dynage,'a') as dynagef:
        #     dynagef.write(str(dynage))
        #     dynagef.write('\n')
        # nx.draw(new_G_small,with_labels = True)
        # plt.show()
    #np.savetxt('datatest.txt',adj_matrix)
    #print(adj_matrix.shape)
        countadj_now=adj_matrix.shape[1]
        countadj.append(adj_matrix.shape[1])
        countedge.append(new_G.number_of_edges())
        with open(filename_center,'a') as centerf:
            centerf.write(str(choice(Jordan_center)))    #Jordan center随机选，按理来说差别可能不大，实际有差别
            centerf.write('\n')
        with open(filename_center1,'a') as centerf1:
            centerf1.write(str(Jordan_center[0]))    #Jordan center选第一个
            centerf1.write('\n')
        with open(filename_node_labels,'a') as labelf:#节点ID作为标签
            for i in new_G.nodes:
                labelf.write(str(i))
                labelf.write('\n')
        graph_labels.append(start_node)
        graph_labels_class.append(partition[start_node])#所属的类
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
    nodetail=117
    #nodelist = [0,2,4,18,9,35,8,41]   #BA100.npy的分类 8类
    #nodelist = [9,2,5,0,15,6,14,31]    #rg_4_100的分类 8类
    #nodelist = [0,1,2,8,10,37,65,11]    #ws_smallworld 8类
    #nodelist=[0, 3, 18, 19, 49, 51, 56, 60, 68, 74, 84, 102, 109, 111, 146, 148, 149, 168, 173, 181, 182, 200, 205, 208, 209, 217, 219, 227, 229, 232, 249, 272, 276, 286, 308, 314, 327, 328, 341, 347, 368, 385, 396, 406, 424, 431, 436, 446, 454, 460, 466, 481, 485, 493, 496]
    #nodelist=[2, 7, 8, 17, 29, 30, 32, 35, 44, 62, 85, 91, 108, 113, 124, 166, 170, 172, 174, 176, 177, 183, 187, 193, 194, 198, 202, 206, 207, 215, 218, 225, 230, 243, 252, 254, 257, 262, 273, 281, 282, 296, 302, 303, 307, 318, 335, 355, 359, 362, 400, 404, 410, 425, 427, 434, 448, 452, 470, 480, 486, 487, 499]
    #nodelist = [0,2,7,10,13,17,74,141,38,39,33]   #food500.npy的分类 11类
    #nodelist = [0, 1, 3, 2, 4, 9, 7, 8, 23, 10, 11, 12, 13, 14, 15, 17, 77, 79, 74, 99, 100, 141, 211, 212, 38, 112, 113, 39, 41, 42, 33, 34, 35]#food500.npy 11类，每类3个节点
    #nodelist = [0, 1, 3, 5, 6, 202, 203, 229, 230, 231, 326, 327, 328, 329, 330, 345, 346, 347, 348, 368, 399, 400, 402, 403, 404, 415, 450, 451, 471]#food500第0类29个节点
    #nodelist = [74, 99, 100, 101, 102, 103, 204, 248, 256, 264, 267, 269, 270, 281, 282, 283, 293, 299, 302, 303, 304, 305, 306, 315, 325, 349, 350, 367, 371, 376, 377, 380, 395, 420, 421, 452, 453, 454, 476, 493]#40j节点
   # nodelist = [10, 11, 12, 24, 25, 26, 27, 28, 43, 54, 55, 59, 62, 65, 66, 81, 83, 84, 96, 105, 107, 172, 174, 180, 181, 182, 183, 184, 186, 188, 205, 207, 232, 233, 237, 239, 240, 242, 243, 244, 246, 263, 274, 287, 291, 298, 324, 353, 374, 382, 390, 393, 409, 410, 413, 423, 425, 428, 430, 435, 455, 472, 474, 478, 479, 485]
    #nodelist = [0, 1, 5, 6, 9, 16, 30, 31]#dolphins的0类
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
        #f.write('InfectionRate='+str(InfectionRate)+"\n")
        #f.write('Roundtime='+str(Roundtime)+"\n")
        f.write('[a,b]='+str(nodehead)+','+str(nodetail)+"\n")
        #f.write('nodelist='+str(nodelist)+'\n')
        f.write('every node graphs='+str(graphs)+"\n")


def main():

    bmname = 'physician117_cSIR_r4_m100'
    #path = os.path.join('/home/zhang/Documents/pytorch/learn/GraphKernel/rexying_diffpool/diffpool-master/data',bmname)
    path = os.path.join('/home/iot/zcy/usb/copy/new_GNN/new_GNN/diffpool-master/data',bmname)
    #path = os.path.join('data',bmname)#调试时生成的文件夹
    if not os.path.exists(path):
        os.makedirs(path)
    perfix = os.path.join(path,bmname)
    filename_readme = perfix+'readme.txt'
    with open(filename_readme,'w') as f:
        f.write('bmname = '+str(bmname)+"\n")
        f.write('N='+str(N)+"\n")
        f.write('底图='+fname+".npy"+"\n")
        f.write('physician117中验证集，r=4,停止传播'+"\n")
        #f.write('val_datatest'+"\n")

    data=open(filename_readme,'a')
    data_A(path,bmname)
    graph_label(path,bmname)
    graph_indicator(path,bmname)
    graph_label_classfication(path,bmname)

    dis_s=0
    for i in countedge:
        dis_s=dis_s+i
    print('sum of edges:',file=data)
    print(str(dis_s)+'\n',file=data)
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
def graph_label_classfication(datadir,bmname): #分类后的节点标签
    perfix = os.path.join(datadir,bmname)
    filename_graph_labels_class = perfix+ '_graph_labels_class.txt'
    with open(filename_graph_labels_class,'w') as f:
        for i in graph_labels_class:
            f.write(str(i))
            f.write('\n')

if __name__ == "__main__":
    main()
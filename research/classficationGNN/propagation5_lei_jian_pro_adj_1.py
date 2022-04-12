#adj记录成list
#记录所有jc
#复制的程序，与pro1同时运行节省时间
#感染图改成根据感染节点连接所有边
#同时改变node_labels, 
# adj为NxN;

#propagation5_lei_jian_pro进化，SI模型
#考虑边的权重且按照总数来生成传播图
#propagation_pro1_4.py是单张病毒图的程序

#500节点时，如果同时计算其他方法的每张图的中心，很慢

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
from PIL import Image
#变量：B，sn范围,每个sn张数 ，Infectionrate, Roundtime，data文件名

N =217#记得必须改
fname = "anu217"
# B = np.load(fname+".npy")#读取固定的图
# G = nx.Graph(B)
G = nx.read_edgelist('./'+fname+'_weight.txt',nodetype = int,data=(('weight',float),),create_using=nx.Graph())

#partition = community_louvain.best_partition(G)
#np.save("BA500_partition.npy",partition)
partition=np.load(fname+'_p'+'.npy',allow_pickle = True).item()
graph_labels = []
graph_labels_class=[]
countedge = []
countadj = []
part=0.1
InfectionRate = 0.5#概率太大，10轮感染1400个节点
Roundtime = 3
adjall = []
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
    count = [1]
    statechange = []
    edgechange = []
    edgeweight = []
    weight_s = 1
    # while len(I)<=part*len(G.nodes()):
    # #for i in range(Roundtime):
    #     for nbr, datadict in G.adj.items():#遍历G的所有节点，nbr节点名称，datadict与节点相连的边
    #         if int(nbr) in S:
    #             node_adj = 0               #S节点的感染邻接点数
    #             for key in datadict:
    #                 if int(key) in I:
    #                     node_adj=node_adj+1
    #                     edgechange.append(int(key))
    #             rate = 1-(1-InfectionRate)**node_adj
    #             if random.random() <= rate:   #被感染后，节点状态变化，感染图的边增加（周围所有感染节点与该点的连边都算上）
    #                 # for a in edgechange:
    #                 #     new_G_small.add_edge(int(nbr),a)
    #                 statechange.append(int(nbr))
    #             edgechange = []
    #     for i in statechange:
    #         S.remove(i)
    #         I.append(i)
    #     for nbr, datadict in G.adj.items():
    #         if int(nbr) in I:
    #             for key in datadict:
    #                 if int(key) in I:
    #                     new_G_small.add_edge(int(nbr),int(key))
    #     count.append(len(I))
    #     statechange = []
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
                    #     new_G_small.add_edge(int(nbr),a)
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
                        new_G_small.add_edge(int(nbr),int(key))
        # if len(I)==1:    #个别情况下，while可能会陷入死循环
        #     break
        count.append(len(I))
        statechange = []
    perfix = os.path.join(datadir,bmname)
    filename_node_labels = perfix + '_xnode_labels.txt'
    filename_center = perfix + '_jordancenter.txt'
    filename_center1 = perfix + '_jordancenterall.txt'

    # filename_unbet = perfix + '_unbet.txt'
    # filename_discen = perfix + '_discen.txt'
    # filename_dynage = perfix + '_dynage.txt'
    #new_G_small表示感染图
    #new_G表示感染图加上未感染的节点，
    #将new_G中的邻接矩阵扩展到G
    new_G = nx.Graph()
    new_G.add_nodes_from(i for i in range(N))
    new_G.add_nodes_from(new_G_small.nodes())    #不增加单独节点看实验效果如何，max_nodes=100时，max graph size 是否为100
    new_G.add_edges_from(new_G_small.edges())
    #Jordan_center  = nx.center(new_G)#非全连接图不能计算

    if not nx.is_empty(new_G):
        adj_matrix = nx.adjacency_matrix(new_G).todense()
        Jordan_center  = nx.center(new_G_small)
        # #无偏中介中心性
        # bet_cen = nx.betweenness_centrality(new_G_small)#节点的中介中心性
        # deg = new_G_small.degree()#节点的度
        # ub={}
        # for i in bet_cen.keys():
        #     ub[i] = bet_cen[i]/(math.pow(deg[i],0.85))
        # unbiased_betweenness = max(ub, key=lambda x: ub[x]) 
        # #unbiased_betweenness = ub.index(max(ub))#####list中index不是对应的节点编号，因为节点编号不是连续的。还得用字典
        # with open(filename_unbet,'a') as unbetf:
        #     unbetf.write(str(unbiased_betweenness))
        #     unbetf.write('\n')

        # #distance centrality
        # dis_path = dict(nx.shortest_path_length(new_G_small))
        # dis_d={}
        # for k,v in dis_path.items():
        #     dis_s=0
        #     for i in v.values():
        #         dis_s = dis_s+i
        #     dis_d[k] = dis_s
        # distance_centrality = min(dis_d, key=lambda x: dis_d[x]) 
        # with open(filename_discen,'a') as discenf:
        #     discenf.write(str(distance_centrality))
        #     discenf.write('\n')

        # #dynamic ages
        # frozen_graph = nx.freeze(new_G_small)#G被冷冻为frozen_graph，不会改变
        # unfrozen_graph = nx.Graph(frozen_graph)#删除节点在非冷冻图上进行，冷冻图不变
        # AS = nx.adjacency_spectrum(frozen_graph)#邻接矩阵特征值
        # m = np.real(AS).round(4).max()
        # all_nodes = new_G_small.nodes
        # #print(all_nodes)
        # da = {}                             ###!!!!!字典才对
        # for i in all_nodes:
        #     unfrozen_graph.remove_node(i)
        #     AS1 = nx.adjacency_spectrum(unfrozen_graph)
        #     m1 = np.real(AS1).round(4).max()
        #     da[i] = float(format(abs(m-m1)/m,'.4f'))   #单独运算看对不对
        #     unfrozen_graph = nx.Graph(frozen_graph)
        # dynage = max(da, key=lambda x: da[x]) 
        # # dynage=1
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
            #print(type(Jordan_center))#list
            for i in Jordan_center:
                centerf1.write(str(i))    #Jordan center
                centerf1.write(',')
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
    A = nx.to_numpy_matrix(new_G) 
    adjall.append(A)
    # im=Image.fromarray(A)
    # if im.mode == "F":
    #     im = im.convert('L')
    # im.save(str(sn)+'.jpeg')

    return (adj_matrix,countadj_now)

#可以自己造邻接矩阵，行和列的范围从adj_matrix.shape开始增加
#直接生成data_A.txt  边的邻接矩阵
def data_A(datadir,bmname):
    perfix = os.path.join(datadir,bmname)
    filename_A = perfix + '_A.txt'
    filename_node_labels = perfix + '_dre_node_labels.txt'
    sum_ca_now = 0
    graphs=5
    # nodehead=0
    # nodetail=217
    nodelist =  [112, 98, 55, 174, 146, 173, 189, 70, 136, 70, 94, 41, 89, 131, 103, 23, 98, 126, 80, 113, 36, 98, 162, 130, 124, 75, 94, 30, 107, 170, 102, 128, 77, 169, 119, 203, 140, 123, 206, 207, 66, 155, 95, 60, 104, 77, 198, 192, 198, 6, 201, 19, 85, 203, 123, 162, 174, 159, 52, 179, 84, 14, 92, 158, 174, 195, 19, 49, 135, 113, 198, 62, 24, 163, 76, 66, 139, 133, 45, 176, 158, 82, 197, 35, 83, 59, 2, 71, 169, 211, 16, 13, 5, 118, 26, 68, 168, 64, 208, 80, 122, 54, 71, 92, 189, 0, 110, 203, 142, 106, 92, 174, 3, 61, 68, 134, 36, 103, 162, 61, 82, 124, 151, 209, 147, 7, 16, 122, 125, 29, 143, 158, 187, 16, 126, 209, 8, 7, 164, 23, 20, 154, 74, 166, 116, 13, 100, 44, 131, 62, 46, 62, 137, 189, 55, 6, 164, 165, 24, 116, 210, 5, 119, 40, 156, 117, 135, 74, 1, 144, 199, 150, 110, 184, 19, 2, 146, 139, 146, 193, 211, 82, 205, 177, 21, 52, 211, 133, 48, 93, 202, 213, 149, 76, 148, 142, 148, 13, 97, 14, 50, 60, 54, 183, 210, 163, 195, 83, 55, 131, 87, 79, 56, 129, 14, 44, 119]
    #nodelist = class2
    with open(filename_A,'w') as f:
        with open(filename_node_labels,'w') as f1: #节点度记录
            for nodesn in nodelist:
            #for nodesn in range(nodehead,nodetail):
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
        #f.write('[a,b]='+str(nodehead)+','+str(nodetail)+"\n")
        f.write('nodelist='+str(nodelist)+'\n')
        f.write('every node graphs='+str(graphs)+"\n")


def main():

    bmname = 'anu217_SI_rm5_test'
    #path = os.path.join('/home/zhang/Documents/pytorch/learn/GraphKernel/rexying_diffpool/diffpool-master/data',bmname)
    #path = os.path.join('/home/iot/zcy/usb/copy/rexying_diffpool/diffpool-master/data',bmname)
    path = os.path.join('/home/iot/zcy/usb/copy/MINIST/MINIST/mydata',bmname)
    #path = os.path.join('data',bmname)#调试时生成的文件夹
    if not os.path.exists(path):
        os.makedirs(path)
    perfix = os.path.join(path,bmname)
    filename_readme = perfix+'readme.txt'
    with open(filename_readme,'w') as f:
        f.write('bmname = '+str(bmname)+"\n")
        f.write('N='+str(N)+"\n")
        f.write('底图='+fname+".npy"+"\n")
        f.write(bmname+'底图，感染节点占part比例时停止传播，z=0.1，包括多种对比方法，分类'+"\n")
        f.write('part='+str(part)+"\n")
        #f.write('val_datatest'+"\n")

    data=open(filename_readme,'a')
    data_A(path,bmname)
    graph_label(path,bmname)
    graph_indicator(path,bmname)
    graph_label_classfication(path,bmname)
    np.save(perfix+ '_adj',adjall)
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
    # filename_adj = perfix+'_adj.txt'
    # with open(filename_adj,'a') as fadj:
    #     for i in range(10):
    #         for j in range(N):
    #             fadj.write(str(adjall[i][j]))
    #             fadj.write('\n')

if __name__ == "__main__":
    main()

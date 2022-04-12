#节点状态做为node_labels
#单张图propagation1_6.py
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

N = 500#记得必须改
fname = "food500"
B = np.load(fname+".npy")#读取固定的图
Gnw = nx.Graph(B)
G = nx.read_edgelist('./'+fname+'_weight.txt',nodetype = int,data=(('weight',float),),create_using=nx.Graph())
obn = int(N*0.5)  #有一半的节点可以观测到
#observenode = random.sample(range(0,N-1),obn)#每次都随机选还是固定呢
#observenode= [387, 312, 379, 258, 17, 320, 33, 448, 302, 204, 405, 469, 34, 446, 418, 77, 426, 49, 109, 59, 487, 371, 158, 237, 140, 478, 473, 301, 470, 329, 122, 396, 333, 61, 173, 15, 374, 186, 452, 32, 150, 178, 261, 125, 27, 360, 251, 4, 318, 372, 93, 72, 28, 457, 128, 463, 114, 54, 149, 14, 462, 210, 113, 455, 141, 20, 321, 99, 388, 359, 351, 409, 291, 271, 227, 451, 143, 328, 284, 74, 304, 344, 496, 129, 289, 190, 306, 147, 468, 355, 89, 453, 429, 75, 94, 29, 184, 111, 9, 349, 299, 174, 376, 354, 416, 256, 13, 257, 265, 65, 249, 44, 217, 415, 461, 317, 481, 242, 253, 450, 364, 58, 489, 391, 76, 345, 454, 182, 16, 279, 402, 80, 222, 87, 12, 46, 471, 430, 300, 434, 248, 97, 439, 135, 8, 494, 126, 0, 96, 200, 81, 88, 212, 444, 123, 121, 493, 485, 230, 91, 73, 358, 214, 330, 127, 313, 267, 216, 180, 90, 474, 45, 384, 133, 235, 482, 266, 183, 366, 95, 175, 228, 460, 456, 124, 368, 472, 339, 153, 244, 309, 145, 335, 69, 232, 492, 419, 56, 138, 43, 283, 375, 268, 51, 63, 319, 377, 286, 433, 432, 262, 398, 479, 458, 105, 401, 103, 288, 132, 327, 169, 102, 334, 498, 119, 223, 356, 404, 19, 116, 336, 326, 62, 26, 315, 144, 269, 264, 278, 176, 193, 331, 118, 181, 423, 195, 495, 234, 310, 445]
#observenode= [i for i in range(62)]
#observenode = [16, 11, 0, 20, 38, 8, 4, 22, 54, 53, 21, 1, 10, 35, 41, 56, 18, 48, 7, 9, 23, 32, 37, 13, 5, 40, 15, 43, 52, 55, 42, 2, 26, 59, 31, 49, 39, 30, 51, 36, 45, 33, 28]#ob0.7
#observenode = [38, 60, 26, 19, 58, 34, 20, 24, 40, 52, 41, 56, 48, 54, 25, 46, 44, 51]#0.3
#observenode=[21, 38, 27, 42, 55, 16, 58, 60, 28, 49, 26, 51, 45, 17, 11, 33, 41, 57, 39, 10, 18, 34, 25, 36, 20, 53, 56, 23, 3, 24, 52]#0.5
observenode =[182, 251, 245, 28, 448, 42, 154, 85, 423, 189, 402, 282, 432, 31, 473, 336, 311, 312, 174, 58, 257, 442, 69, 396, 95, 5, 99, 441, 91, 215, 293, 188, 24, 175, 139, 16, 185, 153, 200, 164, 93, 400, 104, 168, 100, 221, 187, 96, 213, 433, 190, 98, 196, 19, 231, 204, 262, 22, 458, 236, 429, 358, 178, 211, 327, 261, 23, 252, 486, 368, 264, 454, 483, 265, 460, 365, 268, 276, 198, 380, 284, 306, 324, 387, 378, 243, 73, 128, 82, 398, 405, 97, 348, 258, 127, 144, 379, 447, 385, 36, 48, 323, 54, 369, 481, 434, 419, 281, 147, 397, 346, 403, 352, 437, 35, 438, 484, 110, 124, 171, 9, 491, 413, 364, 172, 52, 404, 207, 126, 67, 94, 246, 158, 307, 285, 87, 125, 411, 422, 435, 415, 214, 180, 101, 92, 234, 219, 152, 360, 374, 356, 62, 376, 428, 117, 77, 199, 319, 133, 106, 330, 381, 301, 45, 150, 388, 269, 84, 274, 459, 89, 39, 350, 345, 279, 439, 7, 163, 490, 88, 66, 247, 351, 275, 455, 308, 425, 177, 314, 466, 108, 222, 226, 21, 83, 68, 217, 129, 347, 310, 408, 488, 470, 463, 410, 11, 194, 255, 326, 71, 357, 50, 409, 75, 394, 430, 440, 192, 267, 183, 461, 120, 317, 338, 157, 34, 335, 273, 497, 375, 86, 6, 113, 260, 399, 321, 300, 479, 389, 220, 361, 122, 25, 41, 195, 249, 167, 60, 341, 12]#0.5,food500
print(obn,observenode)
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
def adjConcat(a, b):    #合并对角线矩阵
    lena = len(a)
    lenb = len(b)
    left = np.row_stack((a, np.zeros((lenb, lena),dtype=int)))  # 先将a和一个len(b)*len(a)的零矩阵垂直拼接，得到左半边
    right = np.row_stack((np.zeros((lena, lenb),dtype=int), b))  # 再将一个len(a)*len(b)的零矩阵和b垂直拼接，得到右半边
    result = np.hstack((left, right))  # 将左右矩阵水平拼接
    return result
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
    for nbr, datadict in G.adj.items():
        if int(nbr) in observenode:
            for key in datadict:
                if int(key) in observenode:
                    ob_G.add_edge(int(nbr),int(key))
    relabel_ob_G = nx.Graph()
    mapping={}
    relabel_ob_G_x={}
    it=0
    for ob_n in ob_G.nodes():
        mapping[ob_n]=it
        if ob_n in I:
            relabel_ob_G_x[it]=2     #I 状态
        else:
            relabel_ob_G_x[it]=1      #S状态
        it+=1
    relabel_ob_G=nx.relabel_nodes(ob_G, mapping)     #此时两种图的节点命名应该是不同的

    g_n_i=len(relabel_ob_G_x)
    for g_n in observenode:
        if g_n not in ob_G.nodes():
            if g_n in I:
                relabel_ob_G_x[g_n_i]=2
            else:
                relabel_ob_G_x[g_n_i]=1
            g_n_i +=1
    #print("relabel_ob_G_x:",relabel_ob_G_x)
    
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
    # new_G = nx.Graph()
    # new_G.add_nodes_from(i for i in range(N))
    # new_G.add_nodes_from(new_G_small.nodes())    #不增加单独节点看实验效果如何，max_nodes=100时，max graph size 是否为100
    # new_G.add_edges_from(new_G_small.edges())
    # #Jordan_center  = nx.center(new_G)#非全连接图不能计算

    if not nx.is_empty(new_G_small):
        adj_matrix_relabel = nx.adjacency_matrix(relabel_ob_G).todense()   #为了获得adj与节点状态相对应的A和X
        island = len(observenode)-len(ob_G.nodes())
        adj_matrix = adjConcat(adj_matrix_relabel,np.zeros((island,island),dtype=int))
        Jordan_center  = nx.center(new_G_small)

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
        countedge.append(Gnw.number_of_edges())
        with open(filename_center,'a') as centerf:
            centerf.write(str(choice(Jordan_center)))    #Jordan center随机选，按理来说差别可能不大，实际有差别
            centerf.write('\n')
        with open(filename_center1,'a') as centerf1:
            centerf1.write(str(Jordan_center[0]))    #Jordan center选第一个
            centerf1.write('\n')
        with open(filename_node_labels,'a') as labelf:#节点ID作为标签
            for k,v in relabel_ob_G_x.items():
                labelf.write(str(v))
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
    graphs=50
    nodehead=0
    nodetail=500
    with open(filename_A,'w') as f:
        with open(filename_node_labels,'w') as f1: #节点度记录
            #for nodesn in nodelist:
            for nodesn in range(nodehead,nodetail):
                for j in range(graphs):
                    adj,ca_now=genGraph(nodesn,datadir,bmname)
                    if len(adj):                      #图为非空，才进行下一步
                        coo_A=coo_matrix(adj)   #邻接矩阵的边的行/列的坐标
                        edge_index = [coo_A.row+1,coo_A.col+1]
                        #node_labels(adj)
                        a=np.array(adj)
                        a=np.sum(a,axis=1)
                        a=a.tolist()
                        for i in range(len(a)):
                            f1.write(str(a[i]))
                            f1.write('\n')
                        if len(countadj)==1:
                            for i in range(len(edge_index[1])):
                                f.write(str(edge_index[0][i])+','+str(edge_index[1][i]))
                                f.write('\n')
                                #print(str(coo_A.row[i])+','+str(coo_A.col[i]))
                        else:
                            for i in range(len(edge_index[1])):
                                f.write(str(edge_index[0][i]+sum_ca_now)+','+str(edge_index[1][i]+sum_ca_now))
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

    bmname = fname+'_p0.1_ob0.5_m50'
    #path = os.path.join('/home/zhang/Documents/pytorch/learn/GraphKernel/rexying_diffpool/diffpool-master/data',bmname)
    path = os.path.join('/home/iot/zcy/usb/copy/myGCN/data/'+fname+'/'+bmname+'/raw')
    
    #path = os.path.join('data',bmname)#调试时生成的文件夹
    if not os.path.exists(path):
        os.makedirs(path)
    perfix = os.path.join(path,bmname)
    filename_readme = perfix+'readme.txt'
    with open(filename_readme,'w') as f:
        f.write('bmname = '+str(bmname)+"\n")
        f.write('N='+str(N)+"\n")
        f.write('底图='+fname+".npy"+"\n")
        f.write(fname+'底图，感染节点占part比例时停止传播，测试集，包括多种对比方法，分5类'+"\n")
        f.write('part='+str(part)+"\n")
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

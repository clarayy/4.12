#生成数据集来测试jordancenter
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
import cv2
#变量：B，sn范围,每个sn张数 ，Infectionrate, Roundtime，data文件名

N =500#记得必须改
fname = "food500"
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
U=[]
for i in range(N):
    if i not in observenode:
        U.append(i)
print(U)
partition=np.load(fname+'_p'+'.npy',allow_pickle = True).item()
graph_labels = []
graph_labels_class=[]
countedge = []
countadj = []
part=0.1
InfectionRate = 0.5#概率太大，10轮感染1400个节点
Roundtime = 3
adjall = []
def weight_jordancenter(sub_jc_G):
    lengths = nx.all_pairs_dijkstra_path_length(sub_jc_G,weight='weight')
    lengths = dict(lengths)
    ec = {}
    #for ei in range(len(lengths)):
    for ei in lengths:       #当观测图的编号不从0按顺序开始时；
        ec[ei]=max(lengths[ei].values())
    radius = min(ec.values())
    p = [v for v in ec if ec[v] == radius]
    return p
def genGraph(sn,datadir,bmname,m):

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
    new_G = nx.Graph()
    new_G_small = nx.Graph()
    sub_new_G_b = nx.Graph()   ##观测到的感染图
    sub_new_G_w = nx.Graph()
    sub_new_G_m = nx.Graph()
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
        for nbr, datadict in G.adj.items():
            if int(nbr) in I :
                if int(nbr) in observenode:
                    for key in datadict:
                        if int(key) in I and int(key) in observenode:
                            sub_new_G_b.add_edge(int(nbr),int(key),weight=G.edges[int(nbr),int(key)]['weight'])
                            sub_new_G_m.add_edge(int(nbr),int(key),weight = 1)
                            sub_new_G_w.add_edge(int(nbr),int(key),weight=1-G.edges[int(nbr),int(key)]['weight'])
                        #elif int(key) not in observenode:
        # if len(I)==1:    #个别情况下，while可能会陷入死循环
        #     break
        count.append(len(I))
        statechange = []
    ob_I=[]
    ob_S=[]
    for i in observenode:
        if i in I:
            ob_I.append(i)
        else:
            ob_S.append(i)
    #print(len(ob_I)+len(ob_S)+len(U))
    for nbr, datadict in G.adj.items():
        if int(nbr) in ob_I:
            for key in datadict:
                if int(key) in ob_I:
                    new_G.add_edge(int(nbr),int(key),weight=6)
                elif int(key) in ob_S:
                    new_G.add_edge(int(nbr),int(key),weight=3)
                elif int(key) in U:
                    new_G.add_edge(int(nbr),int(key),weight=4)
        elif int(nbr) in ob_S:
            for key in datadict:
                if int(key) in ob_S:
                    new_G.add_edge(int(nbr),int(key),weight=0)
                elif int(key) in U:
                    new_G.add_edge(int(nbr),int(key),weight=1)
        elif int(nbr) in U:
            for key in datadict:
                if int(key) in U:
                    new_G.add_edge(int(nbr),int(key),weight=2)
    perfix = os.path.join(datadir,bmname)
    #filename_node_labels = perfix + '_xnode_labels.txt'
    filename_b = perfix + '_jordancenter_b.txt'
    filename_m = perfix + '_jordancenter_m.txt'
    filename_w = perfix + '_jordancenter_w.txt'
    filename_adj = perfix+'_adjdata'
    # filename_unbet = perfix + '_unbet.txt'
    # filename_discen = perfix + '_discen.txt'
    # filename_dynage = perfix + '_dynage.txt'
    #new_G_small表示感染图
    #new_G表示感染图加上未感染的节点，
    #将new_G中的邻接矩阵扩展到G
    new_G = nx.Graph()
    new_G.add_nodes_from(i for i in range(N))
    # new_G.add_nodes_from(new_G_small.nodes())    #不增加单独节点看实验效果如何，max_nodes=100时，max graph size 是否为100
    # new_G.add_edges_from(new_G_small.edges())
    new_G.add_nodes_from(sub_new_G_b.nodes())    #不增加单独节点看实验效果如何，max_nodes=100时，max graph size 是否为100
    new_G.add_edges_from(sub_new_G_b.edges())
    #Jordan_center  = nx.center(new_G)#非全连接图不能计算

    if not nx.is_empty(new_G):
        adj_matrix = nx.adjacency_matrix(new_G).todense()
        ###Jordan_center  = nx.center(new_G_small)    #不考虑权重的jc
        Jordan_center_b = weight_jordancenter(sub_new_G_b)
        Jordan_center_m = weight_jordancenter(sub_new_G_m)
        Jordan_center_w = weight_jordancenter(sub_new_G_w)
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
        with open(filename_b,'a') as centerf:
            for i in Jordan_center_b:
                centerf.write(str(i))    #Jordan center
                centerf.write(',')
            centerf.write('\n')
        with open(filename_m,'a') as centerf2:
            for i in Jordan_center_m:
                centerf2.write(str(i))    #Jordan center
                centerf2.write(',')
            centerf2.write('\n')
        with open(filename_w,'a') as centerf1:
            #print(type(Jordan_center))#list
            for i in Jordan_center_w:
                centerf1.write(str(i))    #Jordan center
                centerf1.write(',')
            centerf1.write('\n')
        # with open(filename_node_labels,'a') as labelf:#节点ID作为标签
        #     for i in new_G.nodes:
        #         labelf.write(str(i))
        #         labelf.write('\n')
        graph_labels.append(start_node)
        #graph_labels_class.append(start_node//100)#所属的类   0-99的分类方法
        graph_labels_class.append(partition[start_node])####k-means  反而没；分类方法
    else:
        adj_matrix=[]
        countadj_now=[]
    A = nx.to_numpy_matrix(new_G)   #
    adjall.append(A)
    if not os.path.exists(filename_adj):
        os.makedirs(filename_adj)
    number = sn*100+m
    cv2.imwrite(filename_adj+'/'+str(number)+'.png',A)
    # im = Image.fromarray(A)
    # im.convert('1').save(filename_adj+'/'+str(sn)+'.jpeg')
    return (adj_matrix,countadj_now)

#可以自己造邻接矩阵，行和列的范围从adj_matrix.shape开始增加
#直接生成data_A.txt  边的邻接矩阵
def data_A(datadir,bmname):
    perfix = os.path.join(datadir,bmname)
    filename_A = perfix + '_A.txt'
    filename_node_labels = perfix + '_dre_node_labels.txt'
    sum_ca_now = 0
    graphs=10
    nodehead=0
    nodetail=500
    # class0= [0, 1, 2, 3, 4, 5, 6, 7, 9, 11, 24, 25, 26, 28, 31, 43, 46, 47, 48, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 65, 66, 67, 68, 70, 71, 72, 73, 75, 76, 78, 80, 82, 83, 88, 89, 92, 93, 94, 95, 96, 97, 98, 100, 101, 103, 104, 105, 107, 109, 144, 166, 170, 172, 174, 175, 177, 178, 180, 181, 182, 183, 184, 186, 188, 202, 203, 205, 207, 208, 211, 212, 213, 214, 215, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 239, 240, 244, 245, 246, 249, 258, 260, 261, 262, 263, 265, 268, 271, 273, 274, 275, 276, 286, 290, 291, 296, 298, 310, 326, 327, 328, 329, 330, 335, 345, 346, 347, 348, 363, 364, 368, 372, 374, 381, 382, 384, 385, 386, 387, 390, 393, 395, 396, 398, 402, 403, 411, 413, 415, 423, 424, 425, 426, 427, 428, 429, 430, 432, 435, 440, 450, 451, 455, 461, 468, 469, 470, 471, 474, 478, 479, 481, 482, 485, 487, 495]
    # class1= [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 64, 69, 74, 77, 79, 85, 99, 102, 110, 111, 134, 138, 161, 162, 163, 164, 167, 168, 169, 171, 173, 191, 192, 193, 194, 198, 204, 247, 252, 256, 259, 264, 267, 269, 270, 272, 281, 282, 283, 292, 293, 294, 299, 302, 303, 304, 305, 306, 315, 323, 325, 349, 350, 367, 369, 370, 371, 376, 377, 383, 394, 401, 416, 417, 418, 419, 420, 421, 449, 452, 453, 454, 458, 459, 473, 475, 476, 486, 490, 493]
    # class2= [33, 34, 35, 36, 37, 38, 49, 112, 113, 116, 118, 119, 120, 121, 122, 124, 126, 127, 129, 130, 131, 132, 135, 136, 137, 139, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 189, 216, 217, 218, 254, 255, 277, 278, 288, 300, 301, 308, 309, 311, 312, 313, 314, 317, 318, 319, 336, 337, 338, 339, 343, 344, 373, 378, 379, 380, 388, 389, 397, 399, 400, 404, 405, 406, 407, 412, 437, 462, 463, 464, 465, 480, 483, 488, 489, 492, 494, 496, 497, 498, 499]
    # class3= [8, 10, 12, 27, 29, 30, 32, 39, 40, 41, 42, 44, 45, 81, 84, 86, 87, 90, 91, 106, 108, 114, 115, 117, 123, 125, 128, 133, 140, 141, 142, 143, 165, 176, 179, 185, 187, 190, 195, 196, 197, 199, 200, 201, 206, 209, 210, 219, 220, 221, 222, 238, 241, 242, 243, 248, 250, 251, 253, 257, 266, 279, 280, 284, 285, 287, 289, 295, 297, 307, 316, 320, 321, 322, 324, 331, 332, 333, 334, 340, 341, 342, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 365, 366, 375, 391, 392, 408, 409, 410, 414, 422, 431, 433, 434, 436, 438, 439, 441, 442, 443, 444, 445, 446, 447, 448, 456, 457, 460, 466, 467, 472, 477, 484, 491]
    class0= [33, 34, 35, 36, 37, 38, 49, 112, 113, 116, 118, 119, 120, 121, 122, 124, 126, 127, 129, 130, 131, 132, 135, 136, 137, 139, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 189, 216, 217, 218, 254, 255, 277, 278, 288, 300, 301, 308, 309, 311, 312, 313, 314, 317, 318, 319, 336, 337, 338, 339, 343, 344, 373, 378, 379, 380, 388, 389, 397, 399, 400, 404, 405, 406, 407, 412, 437, 462, 463, 464, 465, 480, 483, 488, 489, 492, 494, 496, 497, 498, 499]
    class1= [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 64, 69, 74, 77, 79, 85, 99, 102, 110, 111, 134, 138, 161, 162, 163, 164, 167, 168, 169, 171, 173, 191, 192, 193, 194, 198, 204, 247, 252, 256, 259, 264, 267, 269, 270, 272, 281, 282, 283, 292, 293, 294, 299, 302, 303, 304, 305, 306, 315, 323, 325, 349, 350, 367, 369, 370, 371, 376, 377, 383, 394, 401, 416, 417, 418, 419, 420, 421, 449, 452, 453, 454, 458, 459, 473, 475, 476, 486, 490, 493]
    class2= [0, 1, 2, 4, 5, 6, 31, 43, 46, 47, 48, 50, 55, 57, 58, 70, 71, 75, 76, 78, 172, 180, 183, 188, 202, 203, 207, 223, 225, 226, 227, 229, 230, 231, 236, 239, 244, 245, 249, 310, 326, 327, 328, 329, 330, 345, 346, 347, 348, 363, 368, 372, 382, 384, 387, 396, 398, 402, 403, 413, 415, 432, 435, 450, 451, 455, 469, 471, 481, 487]
    class3= [3, 7, 9, 11, 12, 24, 25, 26, 27, 28, 32, 51, 52, 53, 54, 56, 59, 60, 61, 62, 63, 65, 66, 67, 68, 72, 73, 80, 82, 83, 88, 89, 92, 93, 94, 95, 96, 97, 98, 100, 101, 103, 104, 105, 107, 108, 109, 144, 165, 166, 170, 174, 175, 176, 177, 178, 181, 182, 184, 186, 205, 206, 208, 211, 212, 213, 214, 215, 224, 228, 232, 233, 234, 235, 237, 238, 240, 241, 246, 258, 260, 261, 262, 263, 265, 268, 271, 273, 274, 275, 276, 279, 280, 284, 286, 287, 290, 291, 296, 297, 298, 316, 324, 331, 332, 333, 335, 352, 353, 356, 361, 362, 364, 374, 381, 385, 386, 390, 393, 395, 408, 409, 410, 411, 423, 424, 425, 426, 427, 428, 429, 430, 436, 440, 447, 460, 461, 468, 470, 472, 474, 478, 479, 482, 485, 495]
    class4= [8, 10, 29, 30, 39, 40, 41, 42, 44, 45, 81, 84, 86, 87, 90, 91, 106, 114, 115, 117, 123, 125, 128, 133, 140, 141, 142, 143, 179, 185, 187, 190, 195, 196, 197, 199, 200, 201, 209, 210, 219, 220, 221, 222, 242, 243, 248, 250, 251, 253, 257, 266, 285, 289, 295, 307, 320, 321, 322, 334, 340, 341, 342, 351, 354, 355, 357, 358, 359, 360, 365, 366, 375, 391, 392, 414, 422, 431, 433, 434, 438, 439, 441, 442, 443, 444, 445, 446, 448, 456, 457, 466, 467, 477, 484, 491]
    ###97 , 91 , 70 , 146 , 96
    #nodelist = class1

    #for nodesn in nodelist:
    for nodesn in range(nodehead,nodetail):
        for j in range(graphs):
            adj,ca_now=genGraph(nodesn,datadir,bmname,j)


    # with open(filename_A,'w') as f:
    #     with open(filename_node_labels,'w') as f1: #节点度记录
    #         for nodesn in nodelist:
    #         #for nodesn in range(nodehead,nodetail):
    #             for j in range(graphs):
    #                 adj,ca_now=genGraph(nodesn,datadir,bmname,j)
    #                 if len(adj):                      #图为非空，才进行下一步
    #                     coo_A=coo_matrix(adj)   #邻接矩阵的边的行/列的坐标
    #                     edge_index = [coo_A.row,coo_A.col]
    #                     #node_labels(adj)
    #                     a=np.array(adj)
    #                     a=np.sum(a,axis=1)
    #                     a=a.tolist()
    #                     for i in range(len(a)):
    #                         f1.write(str(a[i]))
    #                         f1.write('\n')
    #                     if len(countadj)==1:
    #                         for i in range(len(edge_index[1])):
    #                             f.write(str(coo_A.row[i])+','+str(coo_A.col[i]))
    #                             f.write('\n')
    #                             #print(str(coo_A.row[i])+','+str(coo_A.col[i]))
    #                     else:
    #                         for i in range(len(edge_index[1])):
    #                             f.write(str(coo_A.row[i]+sum_ca_now)+','+str(coo_A.col[i]+sum_ca_now))
    #                             f.write('\n')
    #                             #print(str(coo_A.row[i]+sum_ca_now)+','+str(coo_A.col[i]+sum_ca_now))
    #                     sum_ca_now=sum_ca_now+ca_now
    #/home/zhang/Documents/pytorch/learn/GraphKernel/rexying_diffpool/diffpool-master/data
    filename_readme = perfix + 'readme.txt'
    with open(filename_readme,'a') as f:
        #f.write('InfectionRate='+str(InfectionRate)+"\n")
        #f.write('Roundtime='+str(Roundtime)+"\n")
        f.write('[a,b]='+str(nodehead)+','+str(nodetail)+"\n")
        #f.write('nodelist='+str(nodelist)+'\n')
        f.write('every node graphs='+str(graphs)+"\n")


def main():

    bmname = 'food500_p0.1_ob0.5_jc_m10'
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
        f.write('dolphins底图，感染节点占part比例时停止传播，z=0.1，包括多种对比方法，平均分5类'+"\n")
        f.write('part='+str(part)+"\n")
        #f.write('val_datatest'+"\n")

    data=open(filename_readme,'a')
    data_A(path,bmname)
    graph_label(path,bmname)
    graph_indicator(path,bmname)
    graph_label_classfication(path,bmname)
    #np.save(perfix+ '_adj',adjall)
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

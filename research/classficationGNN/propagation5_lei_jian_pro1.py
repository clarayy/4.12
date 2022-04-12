#记录jc中的一个（随机选，第一个），两种情况
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
#变量：B，sn范围,每个sn张数 ，Infectionrate, Roundtime，data文件名

N = 500#记得必须改
fname = "food500"
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
    filename_center1 = perfix + '_jordancenter1.txt'
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
    graphs=10
    #randint1000个
    # nodelist =  [847, 94, 934, 259, 67, 702, 316, 404, 98, 75, 999, 892, 921, 791, 347, 998, 869, 729, 162, 17, 882, 617, 523, 723, 532, 902, 801, 620, 634, 147, 662, 
    # 168, 192, 45, 947, 667, 134, 104, 606, 648, 587, 943, 844, 128, 929, 888, 725, 246, 6, 521, 545, 910, 866, 483, 46, 89, 473, 534, 991, 502, 258, 264, 955, 362,
    #  601, 292, 326, 329, 271, 872, 816, 774, 46, 561, 237, 839, 8, 953, 646, 603, 779, 10, 289, 931, 155, 361, 246, 529, 714, 433, 154, 84, 693, 410, 769, 791, 646, 
    # 811, 867, 829, 371, 266, 338, 249, 676, 543, 897, 277, 228, 860, 70, 222, 344, 183, 559, 711, 802, 775, 343, 196, 346, 231, 860, 213, 104, 643, 279, 377, 
    # 106, 995, 730, 253, 313, 198, 403, 473, 652, 620, 161, 324, 846, 855, 10, 476, 519, 166, 896, 852, 543, 338, 904, 913, 911, 773, 78, 75, 293, 387, 636, 575, 
    # 683, 847, 999, 993, 441, 994, 338, 818, 239, 441, 685, 1, 406, 467, 430, 668, 846, 347, 729, 156, 952, 948, 648, 245, 202, 313, 577, 745, 600, 559, 343, 
    # 485, 254, 300, 97, 566, 116, 25, 628, 61, 617, 820, 374, 672, 958, 109, 299, 509, 247, 137, 113, 725, 271, 730, 843, 666, 383, 987, 782, 994, 977, 156, 644, 
    # 848, 23, 160, 574, 531, 929, 370, 341, 219, 883, 939, 870, 109, 977, 934, 508, 162, 340, 667, 227, 987, 841, 921, 539, 579, 719, 395, 621, 164, 241, 171, 99,
    #  296, 729, 53, 140, 596, 247, 953, 529, 656, 627, 159, 280, 551, 947, 555, 621, 690, 301, 714, 924, 601, 831, 461, 157, 666, 547, 227, 331, 722, 325, 291, 129, 
    # 834, 827, 145, 980, 94, 328, 672, 36, 716, 824, 667, 583, 547, 155, 545, 32, 576, 877, 288, 266, 124, 200, 460, 583, 979, 607, 842, 741, 965, 103, 836, 994, 
    # 422, 535, 759, 128, 404, 331, 16, 753, 999, 75, 112, 476, 303, 556, 366, 406, 756, 117, 710, 605, 858, 7, 828, 351, 751, 874, 307, 194, 683, 443, 317, 579, 
    # 883, 871, 866, 594, 769, 120, 35, 638, 786, 313, 570, 554, 841, 430, 671, 149, 960, 286, 976, 754, 739, 875, 849, 704, 923, 623, 914, 195, 390, 586, 421, 
    # 365, 963, 11, 577, 836, 678, 345, 517, 636, 761, 773, 920, 86, 357, 15, 126, 94, 862, 168, 315, 30, 849, 343, 122, 332, 224, 849, 883, 871, 469, 856, 336, 
    # 988, 333, 606, 515, 67, 283, 207, 510, 87, 486, 363, 291, 233, 417, 270, 793, 903, 346, 581, 7, 651, 236, 631, 536, 430, 233, 506, 132, 743, 228, 788, 596, 
    # 597, 459, 339, 167, 743, 982, 507, 406, 730, 484, 902, 688, 40, 172, 198, 233, 719, 535, 607, 475, 724, 959, 158, 553, 977, 529, 130, 910, 185, 684, 502, 
    # 460, 912, 370, 498, 713, 352, 913, 137, 664, 639, 590, 388, 568, 754, 450, 299, 441, 951, 550, 240, 330, 385, 713, 158, 798, 83, 188, 444, 384, 472, 394, 
    # 389, 897, 874, 294, 222, 841, 240, 854, 831, 729, 491, 176, 734, 805, 11, 512, 609, 259, 968, 750, 397, 448, 164, 910, 304, 762, 783, 793, 842, 379, 700, 
    # 884, 368, 679, 88, 306, 398, 124, 224, 167, 502, 195, 472, 249, 200, 377, 174, 782, 978, 90, 556, 957, 484, 269, 653, 355, 231, 813, 687, 188, 529, 654,
    #  875, 846, 167, 890, 958, 846, 1000, 741, 574, 189, 118, 401, 378, 530, 198, 61, 442, 220, 404, 945, 190, 659, 227, 129, 862, 354, 208, 914, 10, 290, 63,
    #  783, 455, 682, 492, 832, 322, 412, 843, 101, 942, 569, 46, 173, 126, 940, 282, 364, 869, 554, 263, 842, 679, 256, 221, 256, 836, 355, 991, 98, 275, 738, 
    # 238, 156, 771, 67, 966, 573, 426, 886, 41, 626, 217, 827, 450, 227, 782, 285, 285, 471, 324, 997, 592, 298, 383, 951, 953, 307, 154, 726, 127, 404, 850, 
    # 641, 24, 133, 269, 657, 380, 423, 6, 19, 507, 634, 26, 471, 174, 385, 436, 488, 888, 702, 340, 443, 957, 851, 626, 39, 463, 727, 852, 366, 662, 782, 55, 888,
    #  595, 500, 891, 224, 774, 232, 848, 27, 365, 607, 859, 810, 35, 697, 653, 482, 194, 962, 512, 20, 601, 801, 752, 192, 524, 208, 42, 307, 935, 225, 341, 141, 877, 
    # 493, 977, 80, 784, 173, 182, 442, 414, 684, 686, 117, 763, 248, 158, 359, 863, 901, 305, 731, 338, 810, 204, 755, 100, 956, 504, 370, 33, 65, 934, 727, 38, 357, 
    # 417, 693, 124, 455, 289, 330, 760, 752, 675, 648, 420, 703, 908, 817, 230, 995, 446, 466, 771, 179, 688, 66, 579, 231, 994, 525, 474, 623, 367, 707, 752, 267,
    #  729, 51, 605, 278, 467, 646, 462, 17, 893, 470, 425, 676, 107, 564, 467, 485, 144, 563, 390, 33, 886, 22, 603, 978, 83, 13, 947, 967, 541, 187, 269, 584, 101,
    #  298, 989, 205, 614, 926, 629, 168, 659, 29, 294, 91, 558, 276, 534, 393, 56, 456, 304, 342, 257, 464, 901, 696, 551, 297, 806, 879, 313, 997, 85, 514, 869,
    #  417, 635, 378, 650, 361, 488, 929, 11, 535, 614, 733, 771, 236, 699, 275, 81, 980, 730, 630, 449, 8, 723, 899, 765, 585, 507, 844, 76, 648, 702, 400, 346, 
    # 824, 866, 360, 175, 183, 325, 648, 507, 256, 261, 452, 426, 704, 116, 287, 42, 438, 398, 392, 335, 752, 200, 677, 478, 722, 144, 690, 785, 113, 274, 829, 
    # 755, 51, 456, 426, 606, 201, 300, 824, 942, 680, 335, 976, 459, 569, 360, 796, 651, 404, 277, 947, 583, 573, 72, 166, 284, 984, 385, 746, 0, 582, 160, 445,
    #  630, 908, 0, 700, 19, 543, 686, 989, 448, 581, 144, 425, 
    # 410, 387, 561, 973, 969, 530, 605, 893, 649, 582, 57, 660, 914, 410, 579, 368, 938, 130, 606, 915, 803, 120, 928, 61, 708, 20, 975, 71, 163, 163, 693, 965, 735, 822]
    # nodelist = nodelist[50:100]
    # class0= [0, 1, 2, 3, 4, 5, 6, 7, 8, 13, 16, 21, 24, 26, 27, 28, 29, 30, 32, 33, 34, 36, 38, 39, 41, 42, 43, 48, 54, 55, 56, 57, 58, 59, 62, 63, 104, 105, 106, 112, 116, 122, 123, 139, 145, 190, 196, 197]
    # class1= [37, 65, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 85, 121, 133, 134, 137, 150, 152, 153, 156, 157, 160, 167, 171, 172, 173, 174, 175, 185, 186, 187, 189, 201, 202, 204, 207, 209]
    # class2= [15, 17, 18, 19, 20, 25, 31, 35, 45, 46, 47, 49, 50, 51, 52, 53, 60, 61, 66, 67, 69, 72, 89, 90, 91, 92, 95, 96, 97, 98, 99, 100, 101, 102, 103, 113, 114, 115, 117, 118, 119, 120, 126, 130, 132, 135, 146, 147, 154, 159, 161, 162, 169, 170, 176, 178, 188, 191, 198, 199, 203, 214]
    # class3= [9, 10, 11, 12, 14, 22, 23, 44, 86, 107, 108, 109, 110, 111, 128, 129, 131, 136, 158, 205, 206, 210, 212, 216]
    # class4= [40, 64, 68, 70, 71, 84, 87, 88, 93, 94, 124, 125, 127, 138, 140, 141, 142, 143, 144, 148, 149, 151, 155, 163, 164, 165, 166, 168, 177, 179, 180, 181, 182, 183, 184, 192, 193, 194, 195, 200, 208, 211, 213, 215]
    # nodelist = class4
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

    bmname = 'food500_nSI_z0.1_m10_test'
    #path = os.path.join('/home/zhang/Documents/pytorch/learn/GraphKernel/rexying_diffpool/diffpool-master/data',bmname)
    path = os.path.join('/home/iot/zcy/usb/copy/new_GNN/new_GNN_pro/diffpool-master/data',bmname)
    
    #path = os.path.join('data',bmname)#调试时生成的文件夹
    if not os.path.exists(path):
        os.makedirs(path)
    perfix = os.path.join(path,bmname)
    filename_readme = perfix+'readme.txt'
    with open(filename_readme,'w') as f:
        f.write('bmname = '+str(bmname)+"\n")
        f.write('N='+str(N)+"\n")
        f.write('底图='+fname+".npy"+"\n")
        f.write('food500底图，感染节点占part比例时停止传播，测试集，包括多种对比方法，分13类'+"\n")
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

#propagation使用的是从I开始遍历，使S改变状态
#本程序从S开始遍历，感染概率为1-（1-q）^n
#propagation_pro2.py
#改变源节点数，生成对应的图，每个源节点对应6张图（不一定是6）
#每个源节点对应的图数怎么确定？？？？？？？？
#6*10张图用了53s
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

#变量：B，sn范围,每个sn张数 ，Infectionrate, Roundtime，data文件名

N = 100
B = np.load("BA100.npy")#读取固定的图
G = nx.Graph(B)

countedge = []
countadj = []

graph_labels = []
InfectionRate = 0.5#概率太大，10轮感染1400个节点
Roundtime = 4
def genGraph(sn,datadir,bmname):

#感染过程
    node = list(map(int,G.nodes))#图中节点列表，元素转化为整数型
    #node1 = list(set(node))#节点元素从小到大排序
    #print(len(node))
    S = node
    #S=[i+1 for i in node]
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
                        new_G_small.add_edge(int(nbr),a)
                    statechange.append(int(nbr))
                edgechange = []
        for i in statechange:
            S.remove(i)
            I.append(i)
        count.append(len(I))
        statechange = []
    perfix = os.path.join(datadir,bmname)
    filename_node_labels = perfix + '_node_labels.txt'
    filename_center = perfix + '_jordancenter.txt'
    #图为非空时，才有邻接矩阵和countadj_now
    #图为空时，假设邻接矩阵为空，图为空，但没有跳过节点标签 
    #即图的标签数与真实图片数不符

    #将new_G中的邻接矩阵扩展到G
    new_G = nx.Graph()
    new_G.add_nodes_from(i for i in range(N))
    new_G.add_edges_from(new_G_small.edges())
    #Jordan_center  = nx.center(new_G)
    
    if not nx.is_empty(new_G):
        adj_matrix = nx.adjacency_matrix(new_G).todense()
        Jordan_center  = nx.center(new_G_small)
    #np.savetxt('datatest.txt',adj_matrix)
    #print(adj_matrix.shape)
        countadj_now=adj_matrix.shape[1]
        countadj.append(adj_matrix.shape[1])
        countedge.append(new_G.number_of_edges())
        with open(filename_center,'a') as centerf:
            centerf.write(str(Jordan_center[0]))
            centerf.write('\n')
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
    nodetail=10
    #nodelist = [0,2,4,18,9,35,8,41]
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
        f.write('Roundtime='+str(Roundtime)+"\n")
        f.write('[a,b]='+str(nodehead)+','+str(nodetail)+"\n")
        f.write('every node graphs='+str(graphs)+"\n")
'''
#'w'在每次打开f时写入，要先打开文件，否则每次打开文件都在新的文件中写入
#'a+'每次追加到txt中，不如直接写方便，运行一次程序也是接着写
def node_labels(adj):
    with open('node_labels.txt','a+') as f1:
            a=np.array(adj)
            a=np.sum(a,axis=1)
            a=a.tolist()
            for i in range(len(a)):
                f1.write(str(a[i]))
                f1.write('\n')
'''



def main():
    '''
    #生成对角块矩阵b写入datatest.npy，相当于子图拼成大图，当40张图时，维度太大，不行
    b=torch.tensor(genGraph(1))
    for i in range(1,3):
        for j in range(5):#生成了11张图
            adj=genGraph(i)
            a=torch.tensor(adj)
            b=torch.block_diag(b,a)
    np.save('datatest',b)
    data = np.load('datatest.npy')
    print(data.shape[1])
    '''
    bmname = 'wormpro762'
    path = os.path.join('/home/zhang/Documents/pytorch/learn/GraphKernel/rexying_diffpool/diffpool-master/data',bmname)
    #path = os.path.join('data',bmname)
    if not os.path.exists(path):
        os.makedirs(path)
    perfix = os.path.join(path,bmname)
    filename_readme = perfix+'readme.txt'
    with open(filename_readme,'w') as f:
        f.write('N='+str(N)+"\n")

    data=open(filename_readme,'a')
    data_A(path,bmname)
    graph_label(path,bmname)
    graph_indicator(path,bmname)
    '''
    #countadj写入txt
    with open('countadj.txt','w') as f:
        for i in countadj:
            f.write(str(i)) 
            f.write('\n')  
    '''

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

#propagation使用的是从I开始遍历，使S改变状态
#本程序从S开始遍历，感染概率为1-（1-q）^n
#
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import networkx as nx
import os
import random
from itertools import islice
import torch

N = 2000
B = np.load("A.npy")#读取固定的图
G = nx.Graph(B)
for i in G.nodes:
    G.nodes[i]["name"] = i
print(list(G.nodes(data='name')))
'''
#测试用的小图
N = 34
filename = '/home/zhang/Documents/research/graph_python/research/graphtest.txt'
G = nx.Graph()
with open(filename,'r') as file:
    for line in file:
        head,tail=[str(x) for x in line.split( )]
        G.add_edge(head,tail)
#nx.draw(G,with_labels = True)
#plt.show()

'''
countedge = []
countadj = []
def genGraph():
    node_list = []
    edge_list = []
    label_list=[]
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
        start_node = 8#1个初始感染节点
        I.append(start_node)
        S.remove(start_node)
        j=j+1

    print(start_node)

    new_G_small = nx.Graph()
    count = [1]
    statechange = []
    edgechange = []
    InfectionRate = 0.46#概率太大，10轮感染1400个节点
    Roundtime = 20
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
    print(x[:5])
    print(len(I))
    plt.show()  #显示感染曲线
    '''
    node_list.append(I)
    edge_list.extend(new_G.edges)
    for i in I:
        if i != start_node:
            label_list.extend([(i,-1)])
        else:
            label_list.extend([(i,1)])
    #print(len(label_list))
    print(len(I))
    return (node_list, edge_list, label_list)
    '''
    #将new_G中的邻接矩阵扩展到G
    new_G = nx.Graph()
    new_G.add_nodes_from(i for i in range(N))
    new_G.add_edges_from(new_G_small.edges())
    adj_matrix = nx.adjacency_matrix(new_G).todense()
    for i in new_G.nodes:
        new_G.nodes[i]["name"] = i
    print(dict(new_G.nodes(data='name')))
    # with open("nodelabeltest.txt",'a') as f:
    #     for i in new_G.nodes:
    #         f.write(str(i))
    #         f.write('\n')
    #np.savetxt('datatest.txt',adj_matrix)
    print(adj_matrix.shape)
    countadj.append(adj_matrix.shape[1])
    countedge.append(new_G.number_of_edges())
    return (adj_matrix)



#nx.draw(new_G)
#pos = nx.spring_layout(new_G) #为什么报错！！！！！！！！！！
#nx.draw(new_G,pos,node_size = 1)#逗号是中文的  #画图
#plt.show()

'''
dataset = []
for i in range(1):
    print(genGraph())
    dataset.append(genGraph())
'''

def main():
    '''
    b=torch.tensor(genGraph())
    for i in range(5):#生成了11张图
        adj=genGraph()
        a=torch.tensor(adj)
        b=torch.block_diag(b,a)
    np.save('datatest',b)
    '''
    genGraph()
    s=0
    for i in countedge:
        s=s+i
    print('sum of edges:')
    print(s)
    s1=0
    for i in countadj:
        s1=s1+i
    print('sum of adj:')
    print(s1)
if __name__ == "__main__":
    main()

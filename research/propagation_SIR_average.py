#SIR模型
#感染概率0.5，恢复概率0.1
#propagation使用的是从I开始遍历，使S改变状态
#本程序从S开始遍历，感染概率为1-（1-q）^n
#在一张图上同时显示初始图结构和传播感染图，即传播感染图是初始图结构的一部分
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import networkx as nx
import os
import random
from itertools import islice


N = 62
fname = "dolphins"
B = np.load(fname+".npy")#读取固定的图
G = nx.Graph(B)
InfectionRate = 0.7#概率太大，10轮感染1400个节点
RecoverRate = 0.3 #成为R状态
Roundtime = 12
def main():
    num=300
    S,I,R,n,e=average(num)
    print('S:',S)
    print('I:',I)
    print('R:',R)
    print(n)
    print(e)

def average(num):
    sumS=0
    sumI=0
    sumR=0
    sumNode=0
    sumEdge=0
    for i in range(num):
        #感染过程
        node = list(map(int,G.nodes))#图中节点列表，元素转化为整数型
        S = node
        I = []
        R = []
        j=0
        while j<1:
            #start_node = random.choice(node)#1个初始感染节点
            start_node = 0#1个初始感染节点
            I.append(start_node)
            S.remove(start_node)
            j=j+1
        # print("start_node:")
        # print(start_node)

        new_G = nx.Graph()

        count = [1]
        countS = [N-1]
        countR = [0]
        statechange = []
        statechange1 = []
        edgechange = []


        for i in range(Roundtime):
            for nbr, datadict in G.adj.items():#遍历G的所有节点，nbr节点名称，datadict与节点相连的边
                if int(nbr) in S:
                    node_adj = 0               #S节点的感染邻接点数
                    for key in datadict:
                        #if int(key) in I and int(key) not in statechange1:#在同一时间步中，可以先恢复R，同时感染别的S
                        if int(key) in I:
                            node_adj=node_adj+1
                            edgechange.append(int(key))
                    rate = 1-(1-InfectionRate)**node_adj
                    if random.random() <= rate:   #被感染后，节点状态变化，感染图的边增加（周围所有感染节点与该点的连边都算上）
                        for a in edgechange:
                            new_G.add_edge(a,int(nbr))
                        statechange.append(int(nbr))
                    edgechange = []
                if int(nbr) in I and int(nbr)!=start_node:
                    if random.random() <=RecoverRate:                
                        statechange1.append(int(nbr))
                        new_G.remove_node(int(nbr))
            for i in statechange:
                S.remove(i)
                I.append(i)
            for i in statechange1:
                I.remove(i)
                R.append(i)
                if i in new_G.nodes():
                    new_G.remove_node(i)
            # print("new_G.nodes()",new_G.nodes())
            # print("new_G.egdes()",new_G.edges())
            # print("S:",S,"I:",I,"R",R)
            count.append(len(I))
            countS.append(len(S))
            countR.append(len(R))
            statechange = []
            statechange1 = []        
        # print('S:',len(S))
        # print('I:',len(I))
        # print('R:',len(R))
        # print('nodes:',len(new_G.nodes()))
        # print('edges:',len(new_G.edges()))
        sumS = sumS+len(S)
        sumI = sumI+len(I)
        sumR = sumR+len(R)
        sumNode = sumNode+len(new_G.nodes())
        sumEdge = sumEdge+len(new_G.edges())
    aveS = sumS/num
    aveI = sumI/num
    aveR = sumR/num
    aveN = sumNode/num
    aveE = sumEdge/num
    return aveS,aveI,aveR,aveN,aveE

if __name__ == "__main__":
    main()




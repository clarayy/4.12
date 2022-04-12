#propagation使用的是从I开始遍历，使S改变状态
#本程序从S开始遍历，感染概率为1-（1-q）^n
#在一张图上同时显示初始图结构和传播感染图，即传播感染图是初始图结构的一部分
#from research.new_propagation_SI import InfectionRate, Roundtime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import networkx as nx
import os
import random
from itertools import islice
import argparse

# parser = argparse.ArgumentParser(description='SI for argparse')
# parser.add_argument('--Number', '-N', help='总数 属性，非必要参数',required=True)
# parser.add_argument('--name', '-n', help='底图名称，有默认值',required=True)
# parser.add_argument('--Infection', '-g', help='感染率，有默认值',default=0.5)
# parser.add_argument('--Roundtime', '-r', help='轮数，必要参数', default=4)
# args = parser.parse_args()

# N = args.Number
# name = args.name
# InfectionRate = args.Infection
# Roundtime = args.Roundtime
# print(args.Number,args.name,args.Infection,args.Roundtime)
N = 200
#name = "dolphins"
#/home/zhang/Documents/research/graph_python/research/dolphins.npy
B = np.load("/home/zhang/Documents/research/graph_python/research/BA200.npy")#读取固定的图
G = nx.Graph(B)
InfectionRate = 0.5#概率太大，10轮感染1400个节点
Roundtime = 3
def main():
    num=300
    S,I,n,e=average(num)
    print('S:',S)
    print('I:',I)
    print(n)
    print(e)

def average(num):
    sumS=0
    sumI=0
    sumNode=0
    sumEdge=0
    for i in range(num):
        #感染过程
        node = list(map(int,G.nodes))#图中节点列表，元素转化为整数型
        #node1 = list(set(node))#节点元素从小到大排序
        #print(len(node))
        S = node
        I = []

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
                            new_G.add_edge(int(nbr),a)
                        statechange.append(int(nbr))
                    edgechange = []
            for i in statechange:
                S.remove(i)
                I.append(i)
            count.append(len(I))
            statechange = []
        # print('S:',len(S))
        # print('I:',len(I))
        # print('nodes:',len(new_G.nodes()))
        # print('edges:',len(new_G.edges()))
        sumS = sumS+len(S)
        sumI = sumI+len(I)
        sumNode = sumNode+len(new_G.nodes())
        sumEdge = sumEdge+len(new_G.edges())
    aveS = sumS/num
    aveI = sumI/num
    aveN = sumNode/num
    aveE = sumEdge/num
    return aveS,aveI,aveN,aveE

if __name__ == "__main__":
    main()
 
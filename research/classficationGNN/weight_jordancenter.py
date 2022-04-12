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
# 问题 2：无向图的最短路问题（司守奎，数学建模算法与应用，P43，例4.3）
# G2 = nx.Graph()  # 创建：空的 无向图
# G2.add_weighted_edges_from([(1,2,2),(1,3,8),(1,4,1),
#                             (2,3,6),(2,5,1),
#                             (3,4,7),(3,5,5),(3,6,1),(3,7,2),
#                             (4,7,9),
#                             (5,6,3),(5,8,2),(5,9,9),
#                             (6,7,4),(6,9,6),
#                             (7,9,3),(7,10,1),
#                             (8,9,7),(8,11,9),
#                             (9,10,1),(9,11,2),
#                             (10,11,4)])  # 向图中添加多条赋权边: (node1,node2,weight)
# # 两个指定顶点之间的最短加权路径
# minWPath_v1_v11 = nx.dijkstra_path(G2, source=1, target=11)  # 顶点 0 到 顶点 3 的最短加权路径
# print("顶点 v1 到 顶点 v11 的最短加权路径: ", minWPath_v1_v11)
# # 两个指定顶点之间的最短加权路径的长度
# lMinWPath_v1_v11 = nx.dijkstra_path_length(G2, source=1, target=11)  #最短加权路径长度
# print("顶点 v1 到 顶点 v11 的最短加权路径长度: ", lMinWPath_v1_v11)
N =62#记得必须改
fname = "dolphins"
# B = np.load(fname+".npy")#读取固定的图
# G = nx.Graph(B)
G2 = nx.read_edgelist('./'+fname+'_weight.txt',nodetype = int,data=(('weight',float),),create_using=nx.Graph())
def jordancenter(G):
    lengths = nx.all_pairs_dijkstra_path_length(G,weight='weight')
    lengths = dict(lengths)
    # print(lengths)#字典
    # print(len(lengths))
    # print(max(lengths[1].values()))
    ec = {}
    for ei in range(len(lengths)):
        ec[ei]=max(lengths[ei].values())
    radius = min(ec.values())
    p = [v for v in ec if ec[v] == radius]
    # print("ec:",ec)
    # print("p:",p)
    return p
print("jc:",jordancenter(G2))
# e = nx.eccentricity(G2)
# print("e:",e)
pos = nx.spring_layout(G2)  # 用 FR算法排列节点
nx.draw(G2, pos, with_labels=True, alpha=0.5)
labels = nx.get_edge_attributes(G2,'weight')
nx.draw_networkx_edge_labels(G2, pos, edge_labels = labels)
plt.show()
# jc = nx.center(G2)
# print(jc)

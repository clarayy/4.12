from cProfile import label
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import networkx as nx
import os
import random
from itertools import islice
import argparse
from scipy.sparse.coo import coo_matrix
from sklearn.semi_supervised import LabelSpreading

N =62
name = "dolphins"
B = np.load(name+".npy")#读取固定的图
G = nx.Graph(B)
# adj_matrix = nx.adjacency_matrix(G).todense()
# coo_A=coo_matrix(adj_matrix)   #邻接矩阵的边的行/列的坐标
# edge_index = [coo_A.row+1,coo_A.col+1]
# print(len(edge_index))
G = nx.read_edgelist('./'+name+'_weight.txt',nodetype = int,data=(('weight',float),),create_using=nx.Graph())
print(len(G.edges()))
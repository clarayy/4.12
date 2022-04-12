#from propagation_pro import new_G
from networkx.readwrite import json_graph
import json
import numpy as np
from scipy.sparse.coo import coo_matrix
import torch.nn as nn
import torch.nn.functional as F
from tqdm import tqdm_notebook as tqdm
import torch

import networkx as nx
import matplotlib.pyplot as plt
import os.path
#读取对角块矩阵npy（邻接矩阵），将数据集转化为边（node,node）记录下来
# data_A.txt
'''
data = np.load('datatest.npy')
print(data.shape[1])
coo_A=coo_matrix(data)
edge_index = [coo_A.row,coo_A.col]
print(len(edge_index[1]))
with open('dada_A.txt','w') as f:
    for i in range(len(edge_index[1])):#边的总数*2
        f.write(str(coo_A.row[i])+','+str(coo_A.col[i]))#write()中数字必须是str不能是int格式
        f.write('\n')
'''

a = [[0,1,1],[1,0,0],[1,0,0]]
adj = [1,2,3]
new_martix=[]
coo_A=coo_matrix(a)
edge_index = [coo_A.row,coo_A.col]
print(edge_index)
for i in range(len(edge_index[1])):
    for j in adj:
        print(coo_A.row[i]+j)
        print(coo_A.col[i]+j)
#new_martix=a+3
#print(new_martix)     

N=100  
'''
with open('./readme.txt','w') as f:
    f.write('N='+str(N)+"\n")
'''
if not os.path.exists('graph_fenlei_test/test'):
    os.makedirs('graph_fenlei_test/test')
data=open('graph_fenlei_test/test/readmetest.txt','a')
s=0
for i in adj:
    s=s+i
print(s,file=data)
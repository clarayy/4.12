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
#生成node_labels.txt
#用度作为节点的标签

# #data = np.load('datatest.npy')
# data = [[0,1,1,0,1],[1,0,0,1,0],[0,0,0,0,0],[0,1,0,1,0],[1,1,1,1,1]]
# a = np.sum(data,axis=1)
# #print(a)
# with open('node_labels.txt','w') as f:
#     for i in a:
#         f.write(str(i))
#         f.write('\n')

# G = nx.path_graph(4)
# print(list(G.edges))
# H = G.subgraph([0,1,2])#非完全连通图求最大连通子图，此时G与H同时改变
# print(list(H.edges))
# print(list(G.edges))



B=np.load("unconnected.npy")
new_G_small = nx.Graph(B)
pos = nx.spring_layout(new_G_small) #为什么报错！！！！！！！！！！
nx.draw(new_G_small,pos,with_labels = True)#逗号是中文的  #画图
plt.show()
adj = np.array(nx.to_numpy_matrix(new_G_small))
print(adj)
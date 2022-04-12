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
#生成graph_labels.txt
#每张图的源节点看作该图的标签
#暂时不用
with open('data_graph_labels.txt','w') as f:
    i=1
    for val in range(1,11):#每个节点生成的图的数量
        for j in range(5+1):#一个节点对应的随即传播图
            f.write(str(i))
            f.write('\n')
        i=i+1
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
#生成data_graph_indicator.txt
#每张图的节点数
countadj=[]

with open('countadj.txt','r') as f:
    for line in f.readlines():
        countadj.append(line.strip('\n'))
print(countadj[1])
#countadj=[958,977,......]
#总节点数为58193
with open('data/data_graph_indicator.txt','w') as f:
    i=1
    for val in countadj:
        for j in range(int(val)):
            f.write(str(i))
            f.write('\n')
        i=i+1
        


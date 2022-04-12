from dgl.data import MiniGCDataset
import matplotlib.pyplot as plt
import networkx as nx
import dgl
import torch
from dgl.nn.pytorch import GraphConv
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader
dataset = MiniGCDataset(80, 10, 20)
# 上面参数的意思是生成80个图，每个图的最小节点数>=10, 最大节点数<=20
graph, label = dataset[0]  # 拿出第一个数据（图，标签）进行展示
fig, ax = plt.subplots()
nx.draw(graph.to_networkx(), ax=ax)   # 将图转为networkx形式
ax.set_title('Class: {:d}'.format(label))
plt.show()
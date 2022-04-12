#类比karate_club的节点分类GNN，对得到的一张传播图进行训练，已知传播源节点的特征，看其他节点分类聚集的结果是什么
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import networkx as nx
import os
import random
from itertools import islice
import torch
import dgl
N = 1000
B = np.load("1000.npy")#读取固定的图
G = nx.Graph(B)
node = list(map(int,G.nodes))#图中节点列表，元素转化为整数型
#node1 = list(set(node))#节点元素从小到大排序
#print(len(node))
S = node
I = []
j=0
while j<1:
    start_node = random.choice(node)#1个初始感染节点
    I.append(start_node)
    S.remove(start_node)
    j=j+1
print(start_node)

new_G = nx.Graph()
count = [1]
statechange = []
edgechange = []
InfectionRate = 0.046#概率太大，10轮感染1400个节点
Roundtime = 50
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


print(len(I))
print('%d nodes.' % new_G.number_of_nodes())
print('%d edges.' % new_G.number_of_edges())

fig, ax = plt.subplots()
fig.set_tight_layout(False)

pos = nx.spring_layout(new_G)
nx.draw(new_G, pos, with_labels=True,node_size = 5)
plt.show()

def build_graph():
    g = dgl.DGLGraph()
    g.add_nodes(new_G.number_of_nodes())
    edge_list = new_G.edges()
    src,dst = tuple(zip(*edge_list))
    g.add_edges(src,dst)
#    g.add_edges(dst,src)
    return g

nx_G=build_graph()
print('%d nodes.' % nx_G.number_of_nodes())
print('%d edges.' % nx_G.number_of_edges())
# assign features to nodes or edges
import torch
import torch.nn as nn
import torch.nn.functional as F

embed = nn.Embedding(nx_G.number_of_nodes(), 5)  # 1000 nodes with embedding dim equal to 5
nx_G.ndata['feat'] = embed.weight
# print out node 2's input feature
print(nx_G.ndata['feat'][2])

# print out node 10 and 11's input features
print(nx_G.ndata['feat'][[10, 11]])

from dgl.nn.pytorch import GraphConv
class GCN(nn.Module):
    def __init__(self, in_feats, hidden_size, num_classes):
        super(GCN, self).__init__()
        self.conv1 = GraphConv(in_feats, hidden_size)
        self.conv2 = GraphConv(hidden_size, num_classes)

    def forward(self, g, inputs):
        g=dgl.add_self_loop(g)
        h = self.conv1(g, inputs)
        h = torch.relu(h)
        h = self.conv2(g, h)
        return h

# The first layer transforms input features of size of 5 to a hidden size of 5.
# The second layer transforms the hidden layer and produces output features of
# size 2, corresponding to the two groups of the karate club.
net = GCN(5, 5, 2)
inputs = embed.weight
labeled_nodes = torch.tensor([start_node])  # only the instructor and the president nodes are labeled
labels = torch.tensor([1])  # their labels are different
import itertools

optimizer = torch.optim.Adam(itertools.chain(net.parameters(), embed.parameters()), lr=0.01)
all_logits = []
for epoch in range(50):
    logits = net(nx_G, inputs)
    # we save the logits for visualization later
    all_logits.append(logits.detach())
    logp = F.log_softmax(logits, 1)
    # we only compute loss for labeled nodes
    loss = F.nll_loss(logp[labeled_nodes], labels)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    print('Epoch %d | Loss: %.4f' % (epoch, loss.item()))

import matplotlib.animation as animation
import matplotlib.pyplot as plt


def draw(i):
    cls1color = '#00FFFF'
    cls2color = '#FF00FF'
    pos = {}
    colors = []
    for v in range(nx_G.number_of_nodes()):
        pos[v] = all_logits[i][v].numpy()  #pos[0] = [0.2,0.4]
        cls = pos[v].argmax()#返回最大索引  0.4的索引为1
        colors.append(cls1color if cls else cls2color)
    ax.cla()
    ax.axis('off')
    ax.set_title('Epoch: %d' % i)
    nx.draw_networkx(nx_G1.to_undirected(), pos, node_color = colors,node_size = 10,
            with_labels=True, ax=ax)

nx_G1 = nx_G.to_networkx().to_undirected()
pos = nx.spring_layout(nx_G1)
nx.draw(nx_G1,pos,with_labels=True,node_size = 5)
fig = plt.figure(dpi=150)
fig.clf()
ax = fig.subplots()
draw(0)  # draw the prediction of the first epoch
ani = animation.FuncAnimation(fig, draw, frames=len(all_logits), interval=100)
plt.show()
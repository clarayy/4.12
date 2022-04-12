#类比karate_club的节点分类GNN，对得到的一张传播图进行训练，已知传播源节点的特征，看其他节点分类聚集的结果是什么
#生成的图会变，因为相似的的节点会越来越聚合，暂时不需要，只需要得到一张图的embedding

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

f = open('/home/zhang/Documents/research/graph_python/data_G.txt','rb')
preG = nx.read_edgelist(f,delimiter =',')
f.close()
pos = nx.spring_layout(preG)
nx.draw(preG,pos,node_color='b',node_size=1,edge_color = 'b',with_labels = True)
plt.show()

start_node = 882
'''
def build_graph():
    g = dgl.DGLGraph()
    g.add_nodes(117)
    edge_list = [(687, 990), (687, 922), (687, 830), (687, 98), (990, 922), (922, 830), (922, 98), (830, 98), (98, 63), (98, 163), (98, 317), (98, 222), (98, 756), (98, 353), (98, 107), (98, 42), (98, 389), (98, 260), (63, 222), (63, 201), (63, 593), (63, 754), (63, 42), (63, 776), (63, 918), (163, 856), (163, 222), (163, 756), (163, 42), (163, 426), (163, 226), (163, 472), (163, 436), (317, 42), (317, 389), (317, 194), (317, 260), (856, 472), (856, 436), (222, 266), (222, 353), (222, 671), (222, 754), (222, 107), (222, 426), (222, 260), (222, 226), (222, 259), (222, 918), (222, 737), (756, 260), (201, 776), (201, 80), (201, 111), (201, 301), (266, 80), (266, 125), (353, 499), (353, 426), (353, 260), (353, 226), (353, 452), (499, 426), (499, 226), (671, 226), (671, 259), (671, 875), (754, 918), (107, 42), (107, 260), (107, 340), (42, 889), (42, 97), (42, 194), (42, 260), (42, 170), (42, 645), (42, 36), (42, 84), (42, 340), (42, 29), (42, 945), (42, 911), (42, 680), (42, 978), (389, 498), (389, 260), (389, 645), (889, 97), (889, 170), (889, 760), (97, 847), (97, 170), (97, 36), (97, 544), (97, 680), (426, 226), (498, 883), (498, 717), (498, 645), (776, 301), (847, 36), (194, 84), (194, 29), (194, 945), (194, 911), (883, 717), (80, 111), (80, 94), (80, 165), (80, 103), (80, 15), (80, 934), (80, 6), (80, 125), (80, 371), (80, 205), (80, 16), (111, 291), (111, 94), (111, 131), (111, 165), (111, 968), (111, 231), (111, 295), (111, 382), (111, 899), (111, 301), (111, 15), (111, 934), (111, 6), (111, 292), (226, 737), (291, 165), (291, 103), (291, 790), (291, 933), (170, 945), (170, 680), (170, 760), (472, 602), (472, 436), (36, 138), (36, 544), (36, 29), (36, 443), (36, 28), (94, 15), (94, 934), (94, 6), (94, 371), (94, 16), (94, 184), (94, 307), (131, 45), (131, 15), (131, 425), (165, 103), (165, 231), (165, 295), (165, 790), (165, 577), (165, 959), (165, 125), (165, 205), (165, 406), (968, 231), (968, 295), (84, 29), (84, 512), (103, 790), (103, 45), (103, 15), (103, 16), (103, 406), (138, 887), (138, 443), (138, 28), (138, 27), (138, 278), (231, 959), (295, 959), (790, 15), (790, 933), (45, 15), (45, 425), (45, 681), (45, 306), (45, 16), (45, 406), (45, 31), (45, 184), (577, 681), (577, 406), (29, 911), (29, 324), (29, 513), (29, 556), (29, 630), (29, 637), (29, 370), (29, 28), (29, 93), (29, 158), (15, 933), (15, 125), (15, 371), (15, 14), (15, 205), (15, 16), (15, 375), (15, 184), (425, 14), (324, 627), (513, 93), (513, 158), (556, 225), (556, 785), (681, 406), (934, 6), (6, 57), (6, 288), (6, 307), (6, 905), (125, 205), (125, 271), (371, 375), (680, 760), (14, 851), (14, 935), (57, 288), (57, 77), (205, 271), (225, 785), (306, 184), (370, 28), (370, 801), (16, 31), (16, 65), (16, 184), (28, 27), (28, 384), (28, 278), (93, 158), (27, 134), (158, 769), (288, 905)]
    src,dst = tuple(zip(*edge_list))
    g.add_edges(src,dst)
#    g.add_edges(dst,src)
    return g

nx_G=build_graph()
'''
G = dgl.from_networkx(preG)
print('%d nodes.' % G.number_of_nodes())
print('%d edges.' % G.number_of_edges())
# assign features to nodes or edges
import torch
import torch.nn as nn
import torch.nn.functional as F

embed = nn.Embedding(G.number_of_nodes(), 5)  # 66 nodes with embedding dim equal to 5
G.ndata['feat'] = embed.weight
# print out node 2's input feature
print(G.ndata['feat'][2])

# print out node 10 and 11's input features
print(G.ndata['feat'][[10, 11]])

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
labeled_nodes = torch.tensor([40])  # only the instructor and the president nodes are labeled
labels = torch.tensor([1])  # their labels are different
import itertools

optimizer = torch.optim.Adam(itertools.chain(net.parameters(), embed.parameters()), lr=0.01)
all_logits = []
for epoch in range(50):
    logits = net(G, inputs)
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
    for v in range(G.number_of_nodes()):
        pos[v] = all_logits[i][v].numpy()  #pos[0] = [0.2,0.4]
        cls = pos[v].argmax()#返回最大索引  0.4的索引为1
        colors.append(cls1color if cls else cls2color)
    ax.cla()
    ax.axis('off')
    ax.set_title('Epoch: %d' % i)
    nx.draw_networkx(nx_G1.to_undirected(), pos,node_size = 10,
            with_labels=True, ax=ax)

nx_G1 = G.to_networkx().to_undirected()
pos = nx.spring_layout(nx_G1)
nx.draw(nx_G1,pos,with_labels=True,node_size = 5)
fig = plt.figure(dpi=150)
fig.clf()
ax = fig.subplots()
draw(0)  # draw the prediction of the first epoch
ani = animation.FuncAnimation(fig, draw, frames=len(all_logits), interval=100)
plt.show()

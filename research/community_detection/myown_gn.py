import numpy as np
import random
import networkx as nx
from IPython.display import Image
import matplotlib.pyplot as plt
from networkx.algorithms import community
from itertools import islice
k =9
N = 1000
#B = np.load("/home/zhang/Documents/research/graph_python/BA200.npy")#读取固定的图
B = np.load("/home/iot/zcy/usb/copy/research/graph_python/BA1000.npy")#读取固定的图

G = nx.Graph(B)
print(len(G.edges()))
comp = community.girvan_newman(G)
for communities in islice(comp, k):
    a = tuple(sorted(c) for c in communities)
print(a)
dict_par = {}
for i in range(len(a)):#i=0~9
    for value in a[i]:
        # if i not in dict_par:
        #     dict_par[i] = []
        # dict_par[i].append(value)
        dict_par[value] = i
    i = i+1
print(dict_par)
np.save("BA1000_gn10.npy",dict_par)
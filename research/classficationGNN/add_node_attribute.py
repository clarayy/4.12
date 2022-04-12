import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import networkx as nx
import os
import random
from itertools import islice
import json
fname = "BA20"
N=20
B = np.load(fname+".npy")#读取固定的图
G = nx.Graph(B)
d={}   #对图中节点随机生成一个属性作为恢复率
for i in range(N):
    d.setdefault(i,{})['recover']=round(random.random(),2)
print(d)
np.save(fname+'_node_attrs.npy',d)
attrs = np.load(fname+'_node_attrs.npy',allow_pickle = 'TRUE')
print(attrs.item())
nx.set_node_attributes(G,attrs.item())
print(G.nodes[1])
print(G.nodes(data=True))

# 
#  tf = open("dolphins_node_attrs.json","w")
# json.dump(d,tf)
# tf.close()
#tf = open(fname+'_node_attrs.json',"r")
#attrs = json.load(tf)  # 多了 ''，'0':{}没用的
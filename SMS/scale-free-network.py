import matplotlib.pyplot as plt
import csv
import networkx as nx
import os
import random

G = nx.scale_free_graph(400000)
#BA = nx.random_graphs.barabasi_albert_graph(200,1)

pos = nx.spring_layout(G)
nx.draw(G,pos,node_size=10)
plt.show()

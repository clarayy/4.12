import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
#生成400节点scale_free图，输出gexf
G = nx.scale_free_graph(15)
#H = nx.Graph(G)
#nx.write_gexf(H,'un-scale-free.gexf')
A=np.array(nx.adjacency_matrix(G).todense())#生成图的邻接矩阵
pos=nx.spring_layout(G) 
nx.draw(G,pos,with_labels=True)
plt.show()
print('a')
print(A)
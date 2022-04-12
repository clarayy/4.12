#画部分子图
import networkx as nx
import matplotlib.pyplot as plt
G=nx.Graph()
G.add_node(1,id=1000,since='December 2008')
G.add_node(2,id=2000,since='December 2008')
G.add_node(3,id=3000,since='January 2010')
G.add_node(4,id=2000,since='December 2016')
G.add_edge(1,2,since='December 2008')
G.add_edge(1,3,since='February 2010')
G.add_edge(2,3,since='March 2014')
G.add_edge(2,4,since='April 2017')
nx.draw_spectral(G,with_labels=True,node_size=10)
plt.show()
selected_nodes = [n for n,v in G.nodes(data=True) if v['since'] == 'December 2008']  
print (selected_nodes)

selected_edges = [(u,v) for u,v,e in G.edges(data=True) if e['since'] == 'December 2008']
print (selected_edges)
H = G.subgraph(selected_nodes)
nx.draw(H,with_labels=True,node_size=10)
plt.show()
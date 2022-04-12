from networkx.classes.function import subgraph
from networkx.generators.triads import TRIAD_EDGES
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import networkx as nx
import os
import random
from itertools import islice
np.set_printoptions(threshold=np.inf)  
#20节点--3规则树/4规则树
#RG = nx.random_regular_graph(4,20)

# WS = nx.watts_strogatz_graph(200,6,0.1)
# G = nx.Graph(WS)
#social network 中tribes的16节点图
#dolphins中的62节点，159边
#filename = '/home/iot/zcy/usb/copy/research/graph_python/social_network_data/soc-highschool-moreno/soc-highschool-moreno.edges'#hight67
#filename = '/home/iot/zcy/usb/copy/research/graph_python/social_network_data/soc-dolphins/soc-dolphins.mtx'
filename='/home/iot/zcy/social_network/fb-pages-food/fb-pages-food.edges'#620节点
#filename='/home/iot/zcy/social_network/soc-physicians/soc-physicians.edges' #241节点，最大联通子图117节点
#filename='/home/iot/zcy/usb/copy/research/graph_python/social_network_data/soc-wiki-Vote/soc-wiki-Vote.mtx' #889节点
#filename='/home/iot/zcy/usb/copy/research/graph_python/social_network_data/soc-hamsterster/soc-hamsterster.edges' #2426节点，最大联通子图2000节点
#filename = '/home/iot/zcy/usb/copy/research/graph_python/social_network_data/fb-pages-tvshow/fb-pages-tvshow.edges'#3892节点
#filename = '/home/iot/Downloads/reptilia-tortoise-network-fi-2008/reptilia-tortoise-network-fi-2008.edges'  #总283节点最大联通子图38节点
#filename = '/home/iot/Downloads/mammalia-voles-rob-trapping-13/mammalia-voles-rob-trapping-13.edges'#总101节点最大联通子图60节点
#filename = '/home/iot/Downloads/mammalia-voles-plj-trapping-26/mammalia-voles-plj-trapping-26.edges'  #总181,最大171
#filename = '/home/iot/Downloads/mammalia-voles-plj-trapping-24/mammalia-voles-plj-trapping-24.edges' #总115,最大86
#filename='/home/iot/zcy/usb/copy/research/graph_python/social_network_data/fb-pages-politician/fb-pages-politician.edges' #5908节点
#filename = '/home/iot/zcy/usb/copy/research/graph_python/social_network_data/soc-ANU-residence/soc-ANU-residence.edges'#217
#filename = '/home/iot/zcy/usb/copy/research/graph_python/social_network_data/soc-highschool-moreno/soc-highschool-moreno.edges'#70节点
#filename  ='/home/iot/zcy/usb/copy/research/graph_python/social_network_data/soc-advogato/soc-advogato.edges'#5167节点
#filename = '/home/iot/zcy/usb/copy/research/graph_python/social_network_data/p2p-Gnutella08.txt'#6301
#filename = '/home/iot/zcy/usb/copy/research/graph_python/social_network_data/contact-high-school-proj-graph/contact-high-school-proj-graph.txt'#326节点，图画不清楚，边的信息数据不太对
G = nx.Graph()
with open(filename,'r') as file:
    for line in file:
        head,tail=[str(x) for x in line.strip().split(',')]   #\t
        if head !=tail:
            G.add_edge(head,tail)
            #G.add_edge(tail,head)
print("len(nodes):",len(G.nodes()))
print('len(edges):',len(G.edges()))

# nx.draw(G,nx.spring_layout(G),with_labels = True)
# plt.show()
#G.remove_node(57)

# print("len(nodes):",len(G.nodes()))
# nx.draw(G,nx.spring_layout(G),with_labels = True)
# plt.show()
#  #求最大联通子图
# frozen_graph = nx.freeze(G)#G被冷冻为frozen_graph，不会改变
# unfrozen_graph = nx.Graph(frozen_graph)#删除节点在非冷冻图上进行，冷冻图不变
# Gc_node = max(nx.connected_components(G), key=len)   #sub_newG的最大连通子图来求Jordan Center
# #print(Gc_node)
# Gc = unfrozen_graph.subgraph(Gc_node) 

# pos = nx.spring_layout(Gc)
# #print("nodes=:",sorted(Gc.nodes()))
# print("len(nodes):",len(Gc.nodes()))
# print("len(edges):",len(Gc.edges()))
#A = nx.to_numpy_matrix(G) 
#print(A.shape)

# S=np.array(nx.adjacency_matrix(G).todense())
# print(S)
# if A.all() ==S.all():
#     print(True)
#np.save("./Didolphins",S)

# nx.draw(Gc,pos,with_labels = True)
# plt.show()
# plt.subplot(211)
# #subplot=[223,224]
# nG=nx.to_undirected(G)
# print("nG_len(nodes):",len(nG.nodes()))
# print("nG_len(edges):",len(nG.edges()))
""" for c in nx.strongly_connected_components(G): #所有联通子图
#for c in nx.strongly_connected_components(G):
    nodeSet = G.subgraph(c).nodes()
    subgraph = G.subgraph(c)
    #plt.subplot(subplot[0])
    
    print("len(nodes):",len(subgraph.nodes()))
    if len(subgraph.nodes())==214:
        A = nx.to_numpy_matrix(subgraph) 
        #np.save("./anu214",A)
    print(len(subgraph.nodes()))
    print(len(subgraph.edges()))
    nx.draw_networkx(subgraph)
    plt.show() """
#largest_cc = max(nx.strongly_connected_components(G), key=len)  #有向图
largest_cc = max(nx.connected_components(G), key=len)  #无向图
subgraph = G.subgraph(largest_cc)
print(len(subgraph.nodes())) #2068
print(len(subgraph.edges())) #9313
A = nx.to_numpy_matrix(subgraph) 
C = nx.adjacency_matrix(subgraph).todense()
print("diameter:",nx.diameter(subgraph))
degrees = dict(subgraph.degree)
sum_of_edges = sum(degrees.values())/float(len(subgraph))
print(sum_of_edges)
print("len(nodes):",len(subgraph.nodes()))
print('len(edges):',len(subgraph.edges())) 
# print(A[0])
# print(C[0])
#print(A)
#np.savetxt('p2p2068.txt',A)
# np.save("./high67",A)       
# nx.draw_networkx(subgraph)
# plt.show()
# print(len(largest_cc))
    #subplot.pop(0)
#lt.show()
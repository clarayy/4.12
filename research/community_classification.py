import numpy as np
import random
#from IPython.display import Image
import community as community_louvain
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx

# load the karate club graph
#G = nx.karate_club_graph()
N = 400
#B = np.load("/home/zhang/Documents/research/graph_python/BA500.npy")#读取固定的图
B = np.load("/home/iot/zcy/usb/copy/research/graph_python/BA400.npy")#读取固定的图
G = nx.Graph(B)
#first compute the best partition

partition = community_louvain.best_partition(G)
print(partition)
list1 = sorted(partition.items(), key=lambda partition:partition[1])
#print(list1)
class_num = list1[len(list1)-1][1]+1
print("class_num:",class_num)  #最后一个节点对应的类数，但+1才是总的分类数（从0开始）
list2 = []
list3 = []#相同的类作为一个列表放在一起
for i in range(list1[len(list1)-1][1]+1):
    for k,v in partition.items():
        if v==i:
            list2.append(k)
    list3.append(list2)
    list2 = []
#print(list3)
for i in range(len(list3)):
    print(list3[i][0])
for i in range(len(list3)):
    if len(list3[i]) <=3:
        print("小于等于3个节点的分组：",list3[i])   #小于3个节点的小图类不算做一个社区，不计为源节点
# draw the graph
#np.save("BA300_p.npy",partition)   
#print(partition)
# pos = nx.spring_layout(G)
# # color the nodes according to their partition
# cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
# nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40,
#                        cmap=cmap, node_color=list(partition.values()))
# nx.draw_networkx_edges(G, pos, alpha=0.5)
# nx.draw_networkx_labels(G,pos,font_size=8)
# plt.show()
#0,2,7,10,13,17,74,141,38,39,33   food500的11分类
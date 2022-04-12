#from research.propagation_pro2 import graph_indicator
import networkx as nx
import numpy as np
import scipy as sc
import os
import re

datadir='/home/zhang/Documents/research/graph_python'
dataname='data'
prefix = os.path.join(datadir, dataname, dataname)
filename_graph_indic = prefix + '_graph_indicator.txt'
# index of graphs that a given node belongs to
graph_indic={}
with open(filename_graph_indic) as f:
    i=0#i=1
    for line in f:
        line=line.strip("\n")
        graph_indic[i]=int(line)
        i+=1

filename_nodes=prefix + '_node_labels.txt'
node_labels=[]
try:
    with open(filename_nodes) as f:
        for line in f:
            line=line.strip("\n")
            node_labels+=[int(line) - 1]
    num_unique_node_labels = max(node_labels) + 1
except IOError:
    print('No node labels')

filename_node_attrs=prefix + '_node_attributes.txt'
node_attrs=[]
try:
    with open(filename_node_attrs) as f:
        for line in f:
            line = line.strip("\s\n")
            attrs = [float(attr) for attr in re.split("[,\s]+", line) if not attr == '']
            node_attrs.append(np.array(attrs))
except IOError:
    print('No node attributes')
    
label_has_zero = False
filename_graphs=prefix + '_graph_labels.txt'
graph_labels=[]

# assume that all graph labels appear in the dataset 
#(set of labels don't have to be consecutive)
label_vals = []
with open(filename_graphs) as f:
    for line in f:
        line=line.strip("\n")
        val = int(line)
        #if val == 0:
        #    label_has_zero = True
        if val not in label_vals:
            label_vals.append(val)
        graph_labels.append(val)
#graph_labels = np.array(graph_labels)
label_map_to_int = {val: i for i, val in enumerate(label_vals)}
graph_labels = np.array([label_map_to_int[l] for l in graph_labels])
#if label_has_zero:
#    graph_labels += 1

filename_adj=prefix + '_A.txt'
adj_list={i:[] for i in range(1,len(graph_labels)+1)}    
index_graph={i:[] for i in range(1,len(graph_labels)+1)}
num_edges = 0
with open(filename_adj) as f:
    for line in f:
        line=line.strip("\n").split(",")
        e0,e1=(int(line[0].strip(" ")),int(line[1].strip(" ")))
        #print(graph_indic[e0])
        adj_list[graph_indic[e0]].append((e0,e1))
        index_graph[graph_indic[e0]]+=[e0,e1]
        num_edges += 1
for k in index_graph.keys():
    index_graph[k]=[u-1 for u in set(index_graph[k])]
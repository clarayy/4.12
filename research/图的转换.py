import networkx as nx
import matplotlib.pyplot as plt
import random
#图与字典dict,list,numpy,scipy,pandas之间的转换

#从字典生成图 
dod = {0: {1: {'weight': 1}}}   
G = nx.from_dict_of_dicts(dod)  #或G=nx.Graph(dpl) 
plt.subplots(1,1,figsize=(6,3)) 
nx.draw(G, with_labels=True, font_weight='bold') 
plt.axis('on') 
plt.xticks([]) 
plt.yticks([]) 
plt.show() 
 
#图转换为字典 
print(nx.to_dict_of_dicts(G))
print('\n')
#{0: {1: {'weight': 1}}, 1: {0: {'weight': 1}}}

#从列表中创建graph 
dol = {0: [1,2,3]} 
edgelist = [(0, 1),(0,3),(2,3)] 
 
G1 = nx.from_dict_of_lists(dol) #或G=nx.Graph(dol) 
G2=nx.from_edgelist(edgelist) 
#显示graph 
plt.subplots(1,2,figsize=(15,3)) 
plt.subplot(121) 
nx.draw(G1, with_labels=True, font_weight='bold') 
plt.axis('on') 
plt.xticks([]) 
plt.yticks([]) 
plt.subplot(122) 
nx.draw(G2, with_labels=True, font_weight='bold') 
plt.axis('on') 
plt.xticks([]) 
plt.yticks([]) 
plt.show() 
 
#graph转list 
print(nx.to_dict_of_lists(G1)) 
print(nx.to_edgelist(G1)) 
print('\n')
#{0: [1, 2, 3], 1: [0], 2: [0], 3: [0]}
#[(0, 1, {}), (0, 2, {}), (0, 3, {})]

#从numpy创建graph 
import numpy as np 
a = np.reshape(np.random.random_integers(0, 1, size=100), (10, 10))
D = nx.DiGraph(a) 
nx.draw(D, with_labels=True, font_weight='bold') 
plt.axis('on') 
plt.xticks([]) 
plt.yticks([]) 
plt.show() 
 
#graph返回numpy 
G=nx.Graph() 
G.add_edge(1, 2, weight=7.0, body=5) #body可以算作边的属性可以任意命名，只是要他的存储数据
G.add_edge(3, 2,weight=6.0, body=2) 
A1 = nx.to_numpy_matrix(G) 
A2 = nx.to_numpy_recarray(G, dtype=[('weight', float), ('body', int)]) 
print(A1)
print('\n')
print(A2) 
print('\n')
'''
[[0. 7. 0.]
 [7. 0. 6.]
 [0. 6. 0.]] 
 [[(0., 0) (7., 5) (0., 0)]
 [(7., 5) (0., 0) (6., 2)]
 [(0., 0) (6., 2) (0., 0)]]
'''

#从scipy创建graph 
G.clear() 
import scipy as sp 
A = sp.sparse.eye(2, 2, 1) #对角线为1的2x2稀疏矩阵
G = nx.from_scipy_sparse_matrix(A) 
nx.draw(D, with_labels=True, font_weight='bold') 
plt.axis('on') 
plt.xticks([]) 
plt.yticks([]) 
plt.show() 
 
#graph返回scipy 
A = nx.to_scipy_sparse_matrix(G) 
print(A.todense()) #返回稀疏矩阵的np.matrix形式
print('\n')
'''
[[0. 1.]
 [1. 0.]]
 '''
#从pandas创建graph 
G.clear() 
import pandas as pd 
df = pd.DataFrame([[1, 1], [2, 1]]) 
G = nx.from_pandas_adjacency(df) 
nx.draw(D, with_labels=True, font_weight='bold') 
plt.axis('on') 
plt.xticks([]) 
plt.yticks([]) 
plt.show() 
 
#graph返回scipy 
df = nx.to_pandas_adjacency(G) 
print(df) 
'''
    0    1
0  1.0  2.0
1  2.0  1.0
'''
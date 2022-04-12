import matplotlib.pyplot as plt
from networkx import nx
#测试平均节点度
n = 400 # 10 nodes
m = 250# 20 edges
s=0
G = nx.gnm_random_graph(n, m)
for node,degree in G.degree():
    s=degree+s

print(s/10)

nx.draw(G,node_size=3,width=2)
plt.show()

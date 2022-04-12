import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import networkx as nx
import os
import random
from itertools import islice
from collections import Counter
import collections
#计算原始图的最短路径，N越大，p越大

N =171
fname = "trap171"
B = np.load(fname+".npy")#读取固定的图
G = nx.Graph(B)
read_dic = np.load(fname+"_short_path.npy",allow_pickle = True).item()
print(read_dic[0][32])
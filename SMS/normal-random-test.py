#免疫概率a满足标准正态分布，概率测试

import random
import matplotlib.pyplot as plt
walk=[]

count=0
for i in range(1000):
    #a=random.randint(-4,4)#a取0或随机值，概率都在0.5
    a=0
    if a <= random.normalvariate(0,1):
        count=count+1
print(count) 

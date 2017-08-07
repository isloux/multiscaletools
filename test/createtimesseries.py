#!/usr/bin/env python

import pandas as pd
from numpy import random,zeros,transpose
from sys import argv

n=int(argv[1])
k=int(argv[2])
scale=5.0
names=[]
a=zeros((n,k),dtype='float')
for i in range(n):
	s=random.rand()
	for j in range(k):
		a[i][j]+=random.randn()*s*scale
	names.append("s"+str(i+1))
df=pd.DataFrame(transpose(a),columns=names)
df.to_csv("series"+str(n)+".csv",index=None)

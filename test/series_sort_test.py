#!/usr/bin/env python3

from sys import argv,path
path.insert(0,"../python")
from sortseries import *

if len(argv)<2:
    print("Usage:",argv[0],"[series_file].csv")
else:
    cs=CorrelatedSeries(argv[1])
    cs.makepairs()
    print(list(cs.makechain()[0]))

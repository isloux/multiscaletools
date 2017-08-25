#!/usr/bin/env python

from sortseries import *
from sys import argv

cs=CorrelatedSeries(argv[1])
cs.makepairs()
print list(cs.makechain()[0])

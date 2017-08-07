#!/usr/bin/env python

from sortseries import *

cs=CorrelatedSeries("series10.csv")
cs.makepairs()
print cs.chainset1
cs.makechain()
print cs.chainset2[-1]

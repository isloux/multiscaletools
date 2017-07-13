#!/usr/bin/env python

from sortseries import *

cs=CorrelatedSeries("series.csv")
cs.makepairs()
cs.makechain()

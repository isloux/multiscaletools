#!/usr/bin/env python

from collections import namedtuple

class candlestick(namedtuple("candlestick","openq highq lowq closeq")):

	# Declare that tuples are expected
	__slots__=()

	# Je ne sais plus a quoi sert cette fonction
	def __new__(cls,openq,highq,lowq,closeq):
		return super(candlestick,cls).__new__(cls,openq,highq,lowq,closeq)
	#

	def __body__(self):
                if self.openq>self.closeq:
                        low=self.closeq
                        high=self.openq
			shade=1
                else:
                        low=self.openq
                        high=self.closeq
			shade=-1
		return [high,low,shade]

	@property
	def blowq(self):
		return self.__body__()[1]

	@property
	def bhighq(self):
		return self.__body__()[0]

	@property
	def bshadeq(self):
		return self.__body__()[2]

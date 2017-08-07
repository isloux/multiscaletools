#!/usr/bin/env python

"""
	Copyright 2017 Christophe Ramananjaona <cramananjaona AT isloux.com>
	Program for sorting times series two by two according to their covariance
"""

import pandas as pd
from collections import deque
from sys import float_info

MINCOV=-float_info.max

class CovarianceMatrix:

	def __init__(self,cm=pd.DataFrame()):
		self.__cm=cm
		n=len(self.__cm.columns)
		# Save a copy of the full matrix with zeroed diagonal
		self.full=cm.copy()
		for i in cm.columns.tolist():
			self.full[i][i]=MINCOV
                # Zero the upper diagonal of the work matrix
                for i in range(n):
			for j in range(i,n):
				self.__cm.iloc[i][j]=MINCOV

	def locatemax(self):
		row=self.__cm.max().idxmax()
		col=self.__cm.idxmax()[row]
		return row,col

	def drop(self,row,col):
		self.__cm.drop([row,col],inplace=True)
		self.__cm.drop([row,col],axis=1,inplace=True)

	def dropchainselfcovariance(self,chain):
		for row in chain:
			for col in chain:
				self.__cm[row][col]=MINCOV

class CorrelatedSeries:

	def __init__(self,filename):
		# Read time series
		self.__df=pd.read_csv(filename)
		# Compute covariance matrix
		self.cm=CovarianceMatrix(self.__df.cov())
		self.available_names=self.__df.columns.tolist()
		self.chainset1=[]

	def __addtochainbeginning(self,chain_index,elements):
		self.chainset2[chain_index].extendleft(elements)

	def __addtochainend(self,chain_index,elements):
		self.chainset2[chain_index].extend(elements)

	def __getends(self):
		endlist=[]
		for i in self.chainset1:
			endlist.append(i[0])
                        endlist.append(i[-1])
		return endlist

	def __getnode(self,leftnode):
		# Return the maximal covariance of the left over series
		# with the series at the end points of the chains
		return self.cm.full[self.__getends()].loc[leftnode].idxmax()

	def __attachonetoend(self,leftnode,attachnode):
		for i in range(len(self.chainset1)):
			if attachnode in self.chainset1[i]:
				if attachnode==self.chainset1[i][0]:
					self.chainset1[i].extendleft([leftnode])
				elif attachnode==self.chainset1[i][-1]:
					self.chainset1[i].extend([leftnode])
				else:
					raise "Node error"

	def __findchain(self,node):
		for c in self.chainset1:
			if c[0]==node:
				position=0
				return c,position
			elif c[-1]==node:
				position=-1
				return c,position
			else:
				position=-999
		return c,position

	def makepairs(self):
		current_avail_ends=self.available_names
		chain_index=0
		while len(current_avail_ends)>1:
			# Find a maximum
			row,col=self.cm.locatemax()
			self.chainset1.append(deque([row,col]))
			self.cm.drop(row,col)
			current_avail_ends.remove(row)
			current_avail_ends.remove(col)
			chain_index+=1
		if len(current_avail_ends)==1:
			# Find the maximal correlation with an end
			leftnode=current_avail_ends[0]
			self.__attachonetoend(leftnode,self.__getnode(leftnode))

	def makechain(self):
		# Reinitialise the new covariance matrix for the end series
		self.cm=CovarianceMatrix(self.__df.cov())
		# Remove the covariance between elements of a chain
		for c in self.chainset1:
			self.cm.dropchainselfcovariance(c)
		self.chainset2=[]
		current_avail_ends=self.__getends()
		chain_index=0
                while len(current_avail_ends)>2:
                        # Find a maximum
                        row,col=self.cm.locatemax()
			print row,col
			chain1,position1=self.__findchain(row)
			chain2,position2=self.__findchain(col)
			print chain_index,chain1,chain2
			print position1,position2
			# Attach the two ends of the two chains
                        self.chainset2.append(chain1)
			if position1==0:
				if position2==0:
                        		self.__addtochainbeginning(chain_index,list(chain2))
				elif position2==-1:
					niahc2=list(chain2)
					niahc2.reverse()
                        		self.__addtochainbeginning(chain_index,niahc2)
				else:
					raise "Node error"
			elif position1==-1:
                                if position2==0:
                                        self.__addtochainend(chain_index,list(chain2))
                                elif position2==-1:
                                        niahc2=list(chain2)
                                        niahc2.reverse()
                                        self.__addtochainend(chain_index,niahc2)
                                else:
                                        raise "Node error"
			else:
					raise "Node error"
                        self.cm.drop(row,col)
                        current_avail_ends.remove(row)
                        current_avail_ends.remove(col)
			chain_index+=1

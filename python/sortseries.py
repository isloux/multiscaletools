#!/usr/bin/env python

"""
	Copyright 2017 Christophe Ramananjaona <cramananjaona AT isloux.com>
	Program for sorting times series two by two according to their covariance
"""

import pandas as pd
from collections import deque
from sys import float_info
from copy import copy,deepcopy

MINCOV=-float_info.max

class CovarianceMatrix:

	def __init__(self,cm=pd.DataFrame()):
		self.__cm=cm
		self.n=len(self.__cm.columns)
		# Save a copy of the full matrix with zeroed diagonal
		self.full=cm.copy()
		for i in cm.columns.tolist():
			self.full[i][i]=MINCOV
                # Zero the upper diagonal of the work matrix
                for i in range(self.n):
			for j in range(i,self.n):
				self.__cm.iloc[i][j]=MINCOV

	def locatemax(self):
		row=self.__cm.max().idxmax()
		col=self.__cm.idxmax()[row]
		return row,col

	def drop(self,row,col):
		self.__cm.drop([row,col],inplace=True)
		self.__cm.drop([row,col],axis=1,inplace=True)

	def dropchainselfcovariance(self,chain):
		for row in [chain[0],chain[-1]]:
			for col in [chain[0],chain[-1]]:
				self.__cm[row][col]=MINCOV

	def reinit(self):
		self.__cm=self.full
                # Zero the upper diagonal of the work matrix
                for i in range(self.n):
                        for j in range(i,self.n):
                                self.__cm.iloc[i][j]=MINCOV

	def trim(self,nodelist):
		self.__cm=self.__cm[nodelist].copy()
		self.__cm=self.__cm.loc[nodelist].copy()

class ChainSet:

	def __init__(self,initchain=[]):
		self.clist=initchain

        def addtochainbeginning(self,elements):
                self.clist[-1].extendleft(elements)

        def addtochainend(self,elements):
                self.clist[-1].extend(elements)

        def attachonetoend(self,remainingnode,attachnode):
                for i in range(len(self.clist)):
                        if attachnode in self.clist[i]:
                                if attachnode==self.clist[i][0]:
                                        self.clist[i].extendleft([remainingnode])
                                elif attachnode==self.clist[i][-1]:
                                        self.clist[i].extend([remainingnode])
                                else:
                                        raise "Node error"

        def findchain(self,node):
                for c in self.clist:
                        if c[0]==node:
                                position=0
                                return c,position
                        elif c[-1]==node:
                                position=-1
                                return c,position
                        else:
                                position=-999
                return c,position

        def joinchains(self,chain1,chain2,position1,position2):
                # Join two chains in put them at the end of the new chain set list
                self.clist.append(chain1)
                freeends=[]
                if position1==0:
                        freeends.append(chain1[-1])
                        if position2==0:
                                self.addtochainbeginning(list(chain2))
                                freeends.append(chain2[-1])
                        elif position2==-1:
                                freeends.append(chain2[0])
                                niahc2=list(chain2)
                                niahc2.reverse()
                                self.addtochainbeginning(niahc2)
                        else:
                                raise "Node error"
                elif position1==-1:
                        freeends.append(chain1[0])
                        if position2==0:
                                freeends.append(chain2[-1])
                                self.addtochainend(list(chain2))
                        elif position2==-1:
                                freeends.append(chain2[0])
                                niahc2=list(chain2)
                                niahc2.reverse()
                                self.addtochainend(niahc2)
                        else:
                                raise "Node error"
                else:
                        raise "Node error"
                return freeends

class CorrelatedSeries:

	def __init__(self,filename):
		# Read time series
		self.__df=pd.read_csv(filename)
		# Compute covariance matrix
		self.cm=CovarianceMatrix(self.__df.cov())
		self.available_names=self.__df.columns.tolist()
		self.chainset1=ChainSet()

        def __getnode(self,remainingnode,clist):
                # Return the maximal covariance of the left over series
                # with the series at the end points of the chains
                return self.cm.full[self.__getends(clist)].loc[remainingnode].idxmax()

        def __getends(self,clist):
                endlist=[]
                for i in clist:
                        endlist.append(i[0])
                        endlist.append(i[-1])
                return endlist

	def makepairs(self):
		current_avail_ends=copy(self.available_names)
		chain_index=0
		while len(current_avail_ends)>1:
			# Find a maximum
			row,col=self.cm.locatemax()
			self.chainset1.clist.append(deque([row,col]))
			self.cm.drop(row,col)
			current_avail_ends.remove(row)
			current_avail_ends.remove(col)
			chain_index+=1
		if len(current_avail_ends)==1:
			# Find the maximal correlation with an end
			remainingnode=current_avail_ends[0]
			self.chainset1.attachonetoend(remainingnode,self.__getnode(remainingnode,self.chainset1.clist))

	def makechain(self):
		# Reset the covariance matrix to original
		self.cm.reinit()
		# Remove the covariance between elements of a chain
		for c in self.chainset1.clist:
			self.cm.dropchainselfcovariance(c)
		chainset2=ChainSet([[0]])
		current_avail_ends=self.__getends(self.chainset1.clist)
		# Remove the interior nodes
		self.cm.trim(current_avail_ends)
		chain_index=0
                #while len(chainset2.clist[-1])<self.__nseries:
                while len(self.chainset1.clist)>1:
			if chain_index==0:
				# Remove the zero from the list
				chainset2.clist.pop()
                        # Find a maximum
                        row,col=self.cm.locatemax()
			print row,col
			chain1,position1=self.chainset1.findchain(row)
			chain2,position2=self.chainset1.findchain(col)
			print chain_index,chain1,chain2
			print position1,position2
			# Attach the two ends of the two chains into chainset2
			freeends=chainset2.joinchains(chain1,chain2,position1,position2)
                        self.cm.drop(row,col)
                        self.cm.drop(freeends[0],freeends[1])
                        current_avail_ends.remove(row)
                        current_avail_ends.remove(col)
                        current_avail_ends.remove(freeends[0])
                        current_avail_ends.remove(freeends[1])
			self.chainset1.clist.remove(chain1)
			self.chainset1.clist.remove(chain2)
			chain_index+=1
		if len(self.chainset1.clist)==1:
			chainset2.clist.append(self.chainset1.clist[0])	
		self.chainset1=deepcopy(chainset2)
		return chainset2.clist

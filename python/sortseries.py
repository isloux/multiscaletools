#!/usr/bin/env python

"""
	Copyright 2017 Christophe Ramananjaona <cramananjaona AT isloux.com>
	Program for sorting times series two by two according to their covariance
"""

import pandas as pd

class CovarianceMatrix:

	def __init__(self,cm=pd.DataFrame()):
		self.__cm=cm
		n=len(self.__cm.columns)
		# Save a copy of the full matrix with zeroed diagonal
		self.full=cm.copy()
		for i in cm.columns.tolist():
			self.full[i][i]=0.0
                # Zero the upper diagonal of the work matrix
                for i in range(n):
			for j in range(i,n):
                        	self.__cm.iloc[i][j]=0.0

	def locatemax(self):
		row=self.__cm.max().idxmax()
		col=self.__cm.idxmax()[row]
		return row,col

	def drop(self,row,col):
		self.__cm.drop([row,col],inplace=True)
		self.__cm.drop([row,col],axis=1,inplace=True)

class Chainset:

class CorrelatedSeries:

	def __init__(self,filename):
		# Read time series
		self.__df=pd.read_csv(filename)
		# Compute covariance matrix
		self.cm=CovarianceMatrix(self.__df.cov())
		self.available_names=self.__df.columns.tolist()
		self.chainset1=[]

	def __addtochainbeginning(self,chain_index,element):
		self.chainset1[chain_index]=[element]+self.chainset1[chain_index]

	def __addtochainend(self,chain_index,element):
		self.chainset1[chain_index].append(element)

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
					self.chainset1[i]=[leftnode]+self.chainset1[i]
				elif attachnode==i[-1]:
					self.chainset1[i].append(leftnode)
				else:
					raise "Node error"

	def makepairs(self):
		current_avail_ends=self.available_names
		chain_index=0
		while len(current_avail_ends)>1:
			# Find a maximum
			row,col=self.cm.locatemax()
			self.chainset1.append([])
			self.__addtochainbeginning(chain_index,row)
			self.__addtochainend(chain_index,col)
			self.cm.drop(row,col)
			current_avail_ends.remove(row)
			current_avail_ends.remove(col)
			chain_index+=1
		if len(current_avail_ends)==1:
			# Find the maximal correlation with an end
			leftnode=current_avail_ends[0]
			self.__attachonetoend(leftnode,self.__getnode(leftnode))
		print self.chainset1

	def makechain(self):
		# Reinitialise the new covariance matrix for the end series
		self.cm=CovarianceMatrix(self.__df[self.__getends()].cov())
		print self.cm.full
		self.chainset2=[]
		current_avail_ends=self.cm.columns.tolist()
                chain_index=0
                while len(current_avail_ends)>1:
                        # Find a maximum
                        row,col=self.cm.locatemax()
                        self.chainset2.append([])
                        self.__addtochainbeginning(chain_index,row)
                        self.__addtochainend(chain_index,col)
                        self.cm.drop(row,col)
                        current_avail_ends.remove(row)
                        current_avail_ends.remove(col)
                        chain_index+=1


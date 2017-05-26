#/usr/bin/env python
""" 
        Copyright 2016-2017 Christophe Ramananjaona <isloux AT yahoo.co.uk>
"""

from numpy import shape,zeros,pi,cos,sin
from numpy import histogram
from scipy.interpolate import RectBivariateSpline
from sys import float_info

class TwoDCartesianGrid:

	def __init__(self,nx,ny,dx,dy,CompCellCentres=False):
		self.__nx=nx
		self.__ny=ny
		self.__dx=dx
		self.__dy=dy
		if CompCellCentres:
			self.__xc=[dx*0.5]
			for i in range(nx-1):
				ncpo=self.__xc[-1]+dx
				self.__xc.append(ncpo)
			self.__yc=[dy*0.5]
			for j in range(ny-1):
				ncpo=self.__yc[-1]+dy
				self.__yc.append(ncpo)

	def load(self,image,dtp='float'):
		""" The values are defined at the grid centres (xc,yc) """
		(nnx,nny)=shape(image)
		if nnx!=self.__nx:
			raise RuntimeError("Array of wrong size.")
		if nny!=self.__ny:
			raise RuntimeError("Array of wrong size.")
		self.__gridval=zeros((nnx,nny),dtype=dtp)
		self.__dtp=dtp
		for i in range(nnx):
			for j in range(nny):
				self.__gridval[i][j]=image[i][j]

	def __Celldirectionalgrad(self,icx,icy,theta):
		if theta>=pi:
			raise RuntimeError("Wrong angle.")
		endpntminx=self.__xc[icx]-self.__dx*cos(theta)
		endpntmaxx=self.__xc[icx]+self.__dx*cos(theta)
		endpntminy=self.__yc[icy]-self.__dy*sin(theta)
		endpntmaxy=self.__yc[icy]+self.__dy*sin(theta)
		R=2.0*(self.__dx*cos(theta)**2+self.__dy*sin(theta)**2)
		if theta!=0.0 and (theta<=pi*0.5-float_info.epsilon or theta>=pi*0.5+float_info.epsilon):
			endpntminval=self.__finterp(endpntminx,endpntminy)
			endpntmaxval=self.__finterp(endpntmaxx,endpntmaxy)
		elif theta==0.0:
			endpntminval=self.__gridval[icx-1][icy]
			endpntmaxval=self.__gridval[icx+1][icy]
		elif theta>pi*0.5-float_info.epsilon and theta<pi*0.5+float_info.epsilon:
                        endpntminval=self.__gridval[icx][icy-1]
                        endpntmaxval=self.__gridval[icx][icy+1]
		gradient=(endpntmaxval-endpntminval)/R
		return gradient

        def __Initdirectionalgrad(self):
		self.__finterp=RectBivariateSpline(self.__xc,self.__yc,self.__gridval)

	def Imagedirectionalgrad(self,theta):
		""" Does not compute the gradient on the edges """
		if theta!=0.0 and (theta<=pi*0.5-float_info.epsilon or theta>=pi*0.5+float_info.epsilon):
			self.__Initdirectionalgrad()
		self.gradient=zeros((self.__nx,self.__ny),dtype=self.__dtp)
		for i in range(1,self.__nx-1):
			print "Ligne ",i
			for j in range(1,self.__ny-1):
				self.gradient[i][j]=self.__Celldirectionalgrad(i,j,theta)

	def ImageSlopeHistogram(self,nbins):
		""" Builds the histogram of slopes """
		self.hist,bin_edges=histogram(self.gradient,bins=nbins)

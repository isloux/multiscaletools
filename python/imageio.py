#!/usr/bin/env python
""" 
	Copyright 2016 Christophe Ramananjaona <isloux AT yahoo.co.uk>
"""

from PIL import Image
import numpy

def imgread(imgfile,mode="8-bit"):
	img=Image.open(imgfile)
	if mode=="8-bit":
		return numpy.array(img,numpy.uint8)
	elif mode=="16-bit":
		return numpy.array(img,numpy.uint16)
	
def imgwrite(ima,imgfile,mode="8-bit"):
	if mode=="8-bit":
		img=Image.fromarray(ima,"L")
	elif mode=="16-bit":
		img=Image.fromarray(ima,"I;16")
	img.save(imgfile)

#!/usr/bin/env python

from PIL import Image
from numpy import array

def imgread(imgfile):
	img=Image.open(imgfile)
	return(array(img))
	
def imgwrite(ima,imgfile):
	img=Image.fromarray(ima.astype(uint8))
	img.save(imgfile)

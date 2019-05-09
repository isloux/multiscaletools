#!/usr/bin/env python3

from sys import argv
import re
import struct
from numpy import array

def readsepheader(filename):
    lines=open(filename,"r").readlines()
    header={}
    for l in lines:
        allgroups=l.split()
        for i in allgroups:
            mtch=(re.match("(.+)=(.+)",i))
            if mtch!=None:
                header[mtch.group(1)]=mtch.group(2)
    header['esize']=int(header['esize'])
    header['in']=header['in'].strip("\"")
    header['data_format']=header['data_format'].strip("\"")
    #print(header['in'])
    for k in range(1,4):
        index='n'+str(k)
        header[index]=int(header[index])
        #print(header[index])
        index='d'+str(k)
        header[index]=float(header[index])
        #print(header[index])
        index='o'+str(k)
        header[index]=float(header[index])
        #print(header[index])
    return(header)

def by4(f):
        rec='x' # place holder for the while
        while rec:
            rec=f.read(4)
            if rec: yield rec

def readsepdata(filename,n1,n2,n3):
    with open(filename,'rb') as sep:
        a=[]
        for rec in by4(sep):
            pos=struct.unpack('f',rec)
            a.append(pos[0])
        return(array(a).reshape(n3,n2,n1))

def writeascii(filename,header,a):
    f=open(filename,'w')
    f.write("{}\n".format(header['n1']))
    f.write("{}\n".format(header['n2']))
    f.write("{}\n".format(header['n3']))
    f.write("{}\n".format(header['d1']))
    f.write("{}\n".format(header['d2']))
    f.write("{}\n".format(header['d3']))
    f.write("{}\n".format(header['o1']))
    f.write("{}\n".format(header['o2']))
    f.write("{}\n".format(header['o3']))
    f.close()

if __name__=="__main__":
    hdr=readsepheader(argv[1])
    a=readsepdata(hdr['in'],hdr['n1'],hdr['n2'],hdr['n3'])
    writeascii("/dev/shm/temp.file",hdr,a)

#!/usr/bin/env python3

from numpy.random import randn
from databasemanager import *
from time import time
from hashlib import sha256
from array import array
from os.path import exists

def random_walk(n=1000):
    x = [0.0]
    step = randn(n)
    for i in range(1,n):
        x.append(x[i-1]+step[i])
    return x

def hash_name(basename, fileno=0):
    filename = basename + str(fileno) + str(round(time()))
    filename = filename.encode('utf-8')
    return sha256(filename).hexdigest()

if __name__ == "__main__":
    binary = False
    database = binary
    filepath = "../data/"
    nseries = 100
    if exists(filepath):
        base_filename = "randomwalk_"
        series_id = 1
        insert_list = []
        for w in range(nseries):
            if binary:
                hash_filename = hash_name(base_filename, w)
                fullname = filepath + hash_filename + ".bin"
            else:
                fullname = filepath + base_filename + str(w) + ".txt"
            z = random_walk()
            if binary:
                output_file = open(fullname, "wb")
                double_array = array('d', z)
                double_array.tofile(output_file)
                output_file.close()
                insert_list.append([(series_id, hash_filename + '.bin', len(z))])
            else:
                with open(fullname, "w") as fout:
                    for i in range(len(z)):
                        fout.write("{} {}\n".format(i, z[i]))
            series_id += 1
        if database:
            labase = psql_database()
            # Use the default table "test1"
            labase.multiple_insert(insert_list)
            labase.disconnect()
    else:
        print("{} does not exists".format(filepath))

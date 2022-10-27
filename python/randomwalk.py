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

if __name__ == "__main__":
    filepath = "../data/"
    nseries = 100
    if exists(filepath):
        base_filename = "randomwalk_"
        series_id = 1
        insert_list = []
        for w in range(nseries):
            filename = base_filename + str(w) + str(round(time()))
            filename = filename.encode('utf-8')
            hash_filename = sha256(filename).hexdigest()
            fullname = filepath + hash_filename + ".bin"
            z = random_walk()
            output_file = open(fullname, "wb")
            double_array = array('d', z)
            double_array.tofile(output_file)
            output_file.close()
            insert_list.append([(series_id, hash_filename + '.bin', len(z))])
            series_id += 1
        labase = psql_database()
        # Use the default table "test1"
        labase.multiple_insert(insert_list)
        labase.disconnect()
    else:
        print("{} does not exists".format(filepath))

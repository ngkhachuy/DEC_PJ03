import datetime
import os
import sys
import traceback

import pymongo
import numpy as np

import COMMON

if __name__ == '__main__':

    max_rec = 787951
    step = 200000
    count = int(np.round(max_rec/step, 0))
    mod = np.mod(max_rec, step)

    begin = 0
    end = 0
    for i in range(1, count + 1):
        print(begin + end)
        print(end + step * i)

import datetime
import os
import re
import sys
import traceback

import pandas as pd
import pymongo
import numpy as np

import COMMON

if __name__ == '__main__':

    # ------------------------------ Connect to MongoDB
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["TIKI"]
    mycol = mydb["product"]

    print('Thành phần' == 'Thành phần')


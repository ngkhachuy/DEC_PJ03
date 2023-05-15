import datetime
import os
import sys
import traceback

if __name__ == '__main__':
    print(datetime.datetime.now())
    os.execv(sys.executable, ['python'] + sys.argv)
    print("HEEEEEEEEEEEEEEEEEEEEEEEEEEE")

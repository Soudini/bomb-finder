import time
import os
import sys

basedir = os.path.dirname(sys.argv[1] +'/')
if not os.path.exists(basedir):
    os.makedirs(basedir)


time.sleep(2)

open(basedir + '/T_OK', 'a').close()
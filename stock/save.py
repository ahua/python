#!/usr/bin/env python

import os

DATA_DIR = "/var/tmp/data/t"
#DATA_DIR = "/tmp/t2"
FILE_LIST = os.listdir(DATA_DIR)

ALL_LINES = []
CURRENT_ID = 0

for i in FILE_LIST:
    f = os.path.join(DATA_DIR, i)
    code = i[2:8]
    fp = open(f)
    lines = fp.readlines()[2:-1]
    fp.close()

    for li in lines:
        CURRENT_ID += 1
        ALL_LINES.append("%s,%s,%s\n" % (CURRENT_ID, code, li.rstrip()))

OUT = "/tmp/all_stock.data"

f = open(OUT, "w")
f.writelines(ALL_LINES)
f.close()

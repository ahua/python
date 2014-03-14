#!/usr/bin/env python

import sys

lis = []
with open(sys.argv[1]) as fp:
    for li in fp:
        lis.append(li)

max_len = 0
for li in lis:
    if len(li) > max_len:
        max_len = len(li)

for li in lis:
    if len(li) == max_len:
        print li,

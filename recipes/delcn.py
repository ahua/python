#!/usr/bin/env python

import sys
import string 

def usage():
    print "$ prog [-r] f1 f2 ..."

def remove_char(s):
    t = []
    for i in s:
        if i in string.printable:
            t.append(i)
    return "".join(t)

if __name__ == "__main__":
    files = sys.argv[1:]

    for f in files:
        with open(f, "r") as fp:
            lines = [remove_char(i) for i in fp]
        with open(f, "w") as fp:
            fp.writelines(lines)


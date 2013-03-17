#!/usr/bin/env python

import sys
import os
import re

def less3d(filename):
    i = filename.rfind(".")
    suffix = filename[i:]
    name = filename[:i]

    new_name = "%03d" % int(name.replace("lesson","").strip(" "))
    return new_name + suffix

def friends(filename):
    i = filename.rfind(".")
    suffix = filename[i:]
    new_name = re.search("S\d\dE\d\d(\-\d\d)?", filename).group(0)
    return new_name + suffix


def get_new_filename(filename):
    return friends(filename)

def help():
    usage = "$ prog dir"
    print usage
    sys.exit(0)

if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "."
    os.chdir(d)    
    filenames = os.listdir(d)
    for filename in filenames:
        new_filename = get_new_filename(filename)
        print filename, " --> ", new_filename
        #os.rename(filename, new_filename)
        


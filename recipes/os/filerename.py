#!/usr/bin/env python

import sys
import os


def get_new_filename(filename):
    i = filename.rfind(".")
    suffix = filename[i:]
    name = filename[:i]

    new_name = "%03d" % int(name.replace("lesson","").strip(" "))
    return new_name + suffix

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
        print new_filename
        os.rename(filename, new_filename)
        


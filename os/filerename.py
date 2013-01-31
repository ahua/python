#!/usr/bin/env python

import sys
import os


def get_new_filename(filename):
    return "prefix_" + filename


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "."
    
    filenames = os.listdir(d)
    for filename in filenames:
        new_filename = get_new_filename(filename)
        os.rename(filename, filename)


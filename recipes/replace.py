#!/usr/bin/env python

import sys
import gc
REMOVE_JS = True

start_tag = "<script"
end_tag = "</script>"
end_tag_len = len(end_tag)

if __name__ == "__main__":
    filenames = sys.argv[1:]
    for filename in filenames:
        with open(filename, "r") as fp:
            lines = fp.readlines()
        gc.collect()
        removes = []
        newlines = []
        for li in lines:
            gc.collect()
            l = li.find(start_tag)
            r = li.find(end_tag)
            while l >= 0 and r >= 0:
                removes.append(li[l:r+end_tag_len])
                li = li[:l] + li[r+end_tag_len:]
                gc.collect()
                l = li.find(start_tag)
                r = li.find(end_tag)
            newlines.append(li)
        
        for i in removes:
            print i

        gc.collect()
        if REMOVE_JS:
            with open(filename, "w") as fp:
                fp.writelines(newlines)


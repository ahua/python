#!/usr/bin/env python

def attrs(**kwds):
    def decorate(f):
        for k in kwds:
	    setattr(f, k, kwds[k])
        return f
    return decorate

@attrs(version="2.2", author="yhyan")
def test(f):
    print getattr(f, version)

test(object())


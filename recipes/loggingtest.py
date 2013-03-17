#!/usr/bin/env python

import datetime
import socket
import time
import logging

logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('/tmp/test.log')
formatter = logging.Formatter('%(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)

msg = 'HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH1'
def test(uplimit):
    start = datetime.datetime.now()
    n = 0
    while n < uplimit:
        n = n + 1
        logger.warn(msg)
#        time.sleep(0.00001)
    end =  datetime.datetime.now()

    delta = end - start
    total_seconds = delta.days * (24 * 3600) + delta.seconds + delta.seconds / 1000000.0
    RPS = None if total_seconds == 0 else n / total_seconds
    return start, end, total_seconds, uplimit, RPS


print test(10000)
print test(20000)
print test(30000)
print test(40000)
print test(50000)
print test(60000)
print test(70000)
print test(80000)
print test(90000)

print test(100000)
print test(200000)
print test(300000)
print test(400000)
print test(500000)
print test(600000)
print test(700000)
print test(800000)
print test(900000)



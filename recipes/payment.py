#!/usr/bin/env python
# -*- coding: utf-8 -*-

pay = {
    #  month     工资  养老    医疗  住房  个税
    "2013-01": [7800, 149.52, 59.06, 172, 286.94],
    "2012-12": [7800, 149.52, 59.06, 172, 286.94],
    "2012-11": [7800, 149.52, 59.06, 172, 286.94],
    "2012-10": [7800, 149.52, 59.06, 688, 235.34],
    "2012-09": [7800, 149.52, 59.06, 0, 304.14],
    "2012-08": [7800, 299.04, 118.12, 0, 283.38],
    "2012-07": [7800, 0, 0, 0, 325.00]
}

m = "2013-01"
a = pay[m]
p = 1 - (a[1] + a[2] + a[3] + a[4])/a[0]

s = p * 9000
print s
#!/usr/bin/env python

def f(c, x, y):
    i = c / 1000.0 + c * x + c * x * 0.0015
    o = c * (x + y) - c * (x + y) * 0.001 - c * (x + y) * 0.0015
    return o - i


def f1k(x, y):
    return f(1000, x, y)


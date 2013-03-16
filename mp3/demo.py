#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pyxine
import time 

xine = pyxine.Xine()
stream = xine.stream_new()
stream.open("/var/tmp/t.mp3")
stream.play()
time.sleep(1)
l = stream.get_pos_length()
print l

raw_input()



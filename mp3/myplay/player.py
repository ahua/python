#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
from os import path
import ui_cn as ui
import lrc
import pyxine

class g:
    paused = False
    skip = False

def play(f):
    if not path.exists(f):
        ui.throw(u'文件不存在：' + f)
        return
    ui.g.lrcFile = lrc.get_lrc_name(f)
    if not lrc.loadLrc(ui.g.lrcFile):
        ui.g.lrcFile = ''

    xine = pyxine.Xine()
    stream = xine.stream_new()
    stream.open(f)
    stream.play()

    ui.setInfo(f, int(stream.get_pos_length()[2] * 1000))
    g.skip = False
    while not g.skip:
        ui.setTime(int(stream.get_pos_length()[1] * 1000))
        ui.draw()


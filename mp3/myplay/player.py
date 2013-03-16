#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time  # import system modules
from os import path
import ui_cn as ui  # import custom modules
import lrc
import pyxine

class g:  # Glabal Vars
    paused = False
    skip = False

def play(f):  # f: Filename
    if not path.exists(f):
        ui.throw('文件不存在：' + f)
        return
    xine = pyxine.Xine()
    stream = xine.stream_new()
    stream.open(f)

    ui.g.lrcFile = lrc.changeExt(f)
    if not lrc.loadLrc(ui.g.lrcFile):  # No LRC file
        ui.g.lrcFile = ''

    stream.play()
    ui.setInfo(f, int(stream.get_pos_length()[2]))

    g.skip = False
    while not g.skip:
        if not g.paused:
            ui.setTime(int(stream.get_pos_length()[1]))
        else:
            time.sleep(0.1)
        ui.draw()
    
def main():
    
    return 0

if __name__ == '__main__': main()

#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys, traceback
import ui_cn as ui

import player

filelist = sys.argv[1:]
def main():
    global filelist
    noIntro = False
    while True:
        if len(filelist) == 0:
            ui.throw('没有提供任何文件！', True)
        if filelist[0] == '-s':
            noIntro = True
            del filelist[0]
        elif filelist[0] == '-c':
            del filelist[0]
            if len(filelist) == 0:
                ui.throw('错误的参数：-c。', True)
            ui.g.cText = filelist[0]
            del filelist[0]
        elif filelist[0] == '--help':
            ui.showCmdHelp()
            exit()
        else:
            break
    if not noIntro:
        ui.showIntro()
    while True:
        for f in filelist:
            player.play(f)
        ui.showRoll()

ui.initScreen()
try:
    main()
    ui.restoreScreen()
except:
    ui.restoreScreen()
    traceback.print_exc()



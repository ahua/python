#!/usr/bin/env python
#-*- coding: utf-8 -*-

from os import path
import time
import random
import pyxine
from pyxine.constants import XINE_STATUS_IDLE
from pyxine.constants import XINE_STATUS_PLAY 
from pyxine.constants import XINE_STATUS_QUIT 
from pyxine.constants import XINE_STATUS_STOP

from lrc import Lrc
from console import Interface

DEBUG = True

class Player:
    S_IDLE = XINE_STATUS_IDLE
    S_PLAY = XINE_STATUS_PLAY
    S_STOP = XINE_STATUS_STOP    
    
    MODE_CONTINUE = 1
    MODE_RANDOM = 2
    MODE_ONCE = 3
    MODE_REPEAT = 4
    
    
    def __init__(self, mp3_list):
        self.mp3_list = mp3_list
        self.total = len(mp3_list)
        self.i = 0
        self.play_mode = Player.MODE_CONTINUE
        self.lrc = None
        self.xine = pyxine.Xine()
        self.stream = self.xine.stream_new()
        self.play()
        
    def play(self):
        self.stream.open(self.mp3_list[self.i])
        _t = Lrc.get_lrc_filename(self.mp3_list[self.i])
        if _t:
            self.lrc = Lrc(_t) 
        self.stream.play()
            
        while True:
            time.sleep(1)
            pos = int(self.stream.get_pos_length()[1] * 1000)
            Interface.display(self.lrc.get_lyrics(pos), self.mp3_list[self.i])
            if self.status() == self.S_STOP:
                if self.play_mode == Player.MODE_ONCE:
                    break
                else:
                    self.next()
                    self.play()

    def stop(self):
        if self.status() == Player.S_PLAY:
            self.stream.stop()
    
    def status(self):
        return self.stream.status
    
    def next(self):
        if self.play_mode == Player.MODE_CONTINUE:
            self.i = self.i + 1
            if self.i >= self.total:
                self.i = 0
        elif self.play_mode == Player.MODE_REPEAT:
            self.i = self.i 
        elif self.play_mode == Player.MODE_RANDOM:
            self.i = random.randint(0, self.total) 

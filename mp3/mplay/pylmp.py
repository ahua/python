#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys

from player import Player
from lrc import Lrc

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.exit(0)
    mp3_list = sys.argv[1:]
    
    player = Player(mp3_list)
    
    while True:
        r = raw_input()
        if r == "quit\n":
            sys.exit()

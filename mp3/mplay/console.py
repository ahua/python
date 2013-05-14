#!/usr/bin/python
#-*- coding: utf-8 -*-

class Interface:
    P_EMPTY = "     "
    P_CURRENT = "---> "
    @classmethod
    def clear(cls):
        import os
        os.system("clear")

    @classmethod
    def display(cls, lyrics, title=None):
        Interface.clear()
        
        lines = lyrics["lines"]
        pos = lyrics["pos"]

        if title:
            print Interface.P_EMPTY + title

        for i in range(0, len(lines)):
            if i == pos:
                print Interface.P_CURRENT + lines[i][1]
            else:
                print Interface.P_EMPTY + lines[i][1]
        
    

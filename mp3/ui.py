#!/usr/bin/env python
#-*- coding: utf-8 -*-

import curses

def main():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()


def debug():
    print u"测试"
    return None

if __name__ == "__main__":
    main()


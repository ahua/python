#!/usr/bin/env python
#-*- coding: utf-8 -*-

""" 中文界面 """

import curses, traceback, time, locale, player, lrc
from os import path

locale.setlocale(locale.LC_ALL, "")  # Initialize to local environment

class g:  
    scr = None        # screen
    song = ""         # song's filename
    step = 0          # DrawStep; 0: Normal, 1: Paused
    total_time = 0    # song's total time
    current_time = 0  # song's current time
    lrcFile = ''      # LRC filename
    lastInfo = ('', [], None, False, False)  # For checking if it needs to redraw.
    cText = ''        # Custom text

def initScreen():
    g.scr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()

    ''' Curses Pairs:
            1    Default
            2    Error / Title
            3    Message
            4    Normal text
            5    Lrc-lightened
            6    Lrc-unlightened
            7    Console
    '''
    ''' 'COLOR_BLACK', 'COLOR_BLUE', 'COLOR_CYAN', 'COLOR_GREEN', 
        'COLOR_MAGENTA', 'COLOR_RED', 'COLOR_WHITE', 'COLOR_YELLOW'
    '''
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_YELLOW)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
    g.scr.attron(curses.color_pair(1))


def restoreScreen():
    curses.nocbreak()
    curses.echo()
    curses.endwin()


def drawMessage(title, msgs = [], waitKeyMsg = None, beep = False, flash = False):
    """ title: the title on the top like ' === TEXT === '
        msgs: [[str(message), int(color_pair)],[...]]
              You should keep len(msgs) <= 6 if you used 'waitKeyMsg'
              The maximum of the length is 7 (msgs[6]). If you didn't
              use 'waitKeyMsg', you can use msgs[6]
        waitKeyMsg: If it is None, this function will return immediately
                    after drawing, or it will print 'waitKeyMsg' and wait a key.
        beep: It will beep if it is True
        flash: The screen will flash if it is True
    """
    if g.lastInfo == (title, msgs, waitKeyMsg, beep, flash):
        return  # It needn't redraw.
    g.lastInfo = (title, msgs, waitKeyMsg, beep, flash)
    # Do some preparation
    (scry, scrx) = g.scr.getmaxyx()
    assert scrx >= 50  # Console should be big enough
    assert scry > 8  # Console should be big enough
    g.scr.clear()
    # Start to draw
    g.scr.addstr(0, 0, ' ' * scrx * 8)  # Draw background
    # At the first line, draw title in center, with color pair of 2,
    # like this:' === TEXT === '
    g.scr.addstr(0, 1, center2(' %s ' % title, scrx - 2, '='), curses.color_pair(2))
    for i, msg in enumerate(msgs[:7]):
        msg[0] = msg[0].replace('\n','_').replace('\r','_')  # no CR/LF
        if i == 6:
            space = 1
        else:
            space = 2
        msg[0] = limitLen(msg[0], g.scr.getmaxyx()[1] - space * 2)  # Keep it in a line with 'space' spaces in 2 sides
        g.scr.addstr(1 + i, 1, ' ' * (scrx - 2), curses.color_pair(msg[1]))  # Fill this line
        g.scr.addstr(1 + i, space, msg[0], curses.color_pair(msg[1]))  # Draw a message
    if waitKeyMsg is not None:
        waitKeyMsg = limitLen(waitKeyMsg, g.scr.getmaxyx()[1] - 2)
        g.scr.addstr(7, 1, waitKeyMsg, curses.color_pair(1))
    copyright = threelize('(C) bainainfo, 2013.', g.cText, 'yhyan@bainainfo.com', scrx - 2)
    g.scr.addstr(8, 1, copyright, curses.color_pair(7))
    g.scr.refresh()

    if beep == True:
        curses.beep()
    if flash == True:
        for i in range(2):
            curses.flash()
            time.sleep(0.1)
    # Do interactivation
    if waitKeyMsg is not None:
        g.scr.nodelay(False)
        return g.scr.getch()


def generateStatus():
    if g.step == 0:
        msg = '播放中' 
    elif g.step == 1:
        msg = '已暂停'
    else:
        throw('step = %i' % g.step, True)
    # Maximum length of msg on the left-bottom is 10
    msg = msg + ' ' * (10 - len2(msg))  # Add spaces
    # Add a progress bar
    if g.total_time != 0:
        pct = 100 * g.current_time / g.total_time  # pct: Percentage
    else:
        pct = 0
    pctStr = str(pct) + '%'
    if len(pctStr) == 2:
        pctStr = ' ' + pctStr  # Format
    msg = msg + pctStr + ' '
    pbarLen = g.scr.getmaxyx()[1] - len2(msg) - 4
    pbarPos = pbarLen * pct / 100
    pbar = '[' + '=' * pbarPos + ' ' * (pbarLen - pbarPos) + ']'
    msg = msg + pbar
    return msg


def threelize(strLeft, strCenter, strRight, x):
    """ Let three strings join in a line
        x: the width of screen
    """
    maxLen = (x - len2(strCenter)) / 2
    strLine = center2(strCenter, x)
    strLeft = limitLen(strLeft, maxLen)
    if len2(strRight) > maxLen:
        strRight = limitLen(strRight, len2(strRight) - maxLen, True)
    strLine = strLeft + strLine[len2(strLeft):]
    strLine = strLine[:-len2(strRight)] + strRight
    return strLine


def throw(msg, isError = False):  # isError or isWarning; Error will exit, warning will not
    msgs = [['', 2],['', 2],\
            ['发生了一个错误：', 2],\
            [msg, 2]]
    if isError:
        waitKeyMsg = '按任意键退出...'
    else:
        waitKeyMsg = '按任意键继续...'
    # Draw error message with beep and flash
    drawMessage('出错啦', msgs, waitKeyMsg, True, True)
    if isError:
        restoreScreen()
        exit()


def draw():
    g.scr.nodelay(True)
    statMsg = 'MP3 文件：' + path.basename(g.song)
    lrcTitle = '未知歌曲名'
    if g.lrcFile:
        lrcMsg = 'LRC 文件：' + path.basename(g.lrcFile)
        if lrc.g.lrcds.has_key('ti'):
            lrcTitle = lrc.g.lrcds['ti']
        lyrics = lrc.getLrc(g.current_time)
    else:
        lrcMsg = '没有 LRC 文件'
        lyrics = ['提醒：', '找不到 LRC 文件。',\
                "您有没有将其命名为  %s 呢？" % path.basename(lrc.changeExt(g.song))]
    statMsg = threelize(statMsg, lrcTitle, lrcMsg, g.scr.getmaxyx()[1] - 4)
    msgs = [[statMsg, 4],\
            ['', 1],\
            [lyrics[0], 6],\
            [lyrics[1], 5],\
            [lyrics[2], 6],\
            ['', 1],\
            [generateStatus(), 1]]
    drawMessage('LRC MP3 播放器 v0.1', msgs)
    if g.step == 0:
        key = g.scr.getch()
        if key in range(256):
            if chr(key) == 'q':
                exit()
            elif chr(key) == 'p':
                player.g.paused = True
                g.step = 1
                curses.beep()
            elif chr(key) == 's':
                player.g.skip = True
            elif chr(key) == 'h':
                showHelp()
    elif g.step == 1:
        key = g.scr.getch()
        if key in range(256):
            if chr(key) == 'q':
                exit()
            elif chr(key) == 'p':
                player.g.paused = False
                g.step = 0
            elif chr(key) == 'h':
                showHelp()


def setInfo(song, length):
    g.song = song
    g.current_time = 0
    g.total_time = length


def setTime(time):
    g.current_time = time


def showIntro():
    msg = [['欢迎使用 LRC MP3 播放器 v0.1！', 3],\
           ['这个播放器可以播放 mp3 文件，也能显示 lrc 歌词。', 3],\
           ['当然了，歌词必须是 utf8/gbk 编码的（包括 gb2312 等编码）。', 3],['', 3],\
           ['希望你能喜欢！', 3]]
    key = drawMessage('欢迎使用', msg, '按 s 键跳过，其它键继续...')
    if chr(key) == 's':
        return
    msg = [['该软件是由 cjxgm (兰威举) 提出并完成最初代码的。', 3],\
           ['它是在 GPLv3 的许可下发行的，因此它将永远免费和开源！', 3],\
           ['想要了解更多细节，请查看 GPLv3 的拷贝。', 3], ['', 3],\
           ['此软件的版权由克兰软件工作室的 cjxgm (兰威举) 所有。', 2],\
           ['修改请公布源代码，发行请带上此文本！', 2]]
    key = drawMessage('版权声明', msg, '按 s 键跳过，其它键继续...', False, True)
    if chr(key) == 's':
        return
    showHelp()


def showHelp():
    msg = [['h：显示此帮助     q：退出    p：暂停/播放    s：跳过/下一曲', 3], ['注意：按键都是小写的！', 3],\
           ['已知问题：', 4],\
           ['  暂停的反应有点慢。', 2],\
           ['  只支持 utf8/gbk 编码（包括 gb2312 等编码）。', 2],\
           ['  异常退出可能导致tty/终端混乱，需要手动运行 reset 恢复。', 2]]
    drawMessage('帮助', msg, '按任意键退出帮助...')


def showCmdHelp():
    msg = [['', 4], ['pylmp [--help] [-s] mp3文件 [...]', 4],\
           ['  Python 写的文本界面的 LRC MP3 播放器。', 3],\
           ['  --help  显示此帮助。', 2],\
           ['  -s      跳过开头的说明。', 2]]
    drawMessage('命令行帮助', msg, '按任意键退出帮助...')


def showRoll():  # Show 'Rolling back' dialog
    msgs = [['', 2], ['', 2], ['列表中的所有歌曲都已播放完毕。', 4],\
            ['要回滚（从头开始播放）吗？', 3]]
    key = drawMessage('回滚咯', msgs, '按 q 键退出，其它键回滚...', True)
    if chr(key) == 'q':
        exit()


def len2(string):
    """ For the calculation of the length of CJK characters """
    try:
        l = len(string.decode('utf8').encode('gbk'))
    except:
        l = 8  # The length of '编码错误'
    return l


def limitLen(string, maxLen, left = False):
    """ For the calculation of the length of CJK characters """
    s = '编码错误'
    if left:
        try:
            s = string.decode('utf8').encode('gbk')[maxLen:].decode('gbk').encode('utf8')
        except:
            try:
                s = string.decode('utf8').encode('gbk')[maxLen + 1:].decode('gbk').encode('utf8')
            except:
                pass
    else:
        try:
            s = string.decode('utf8').encode('gbk')[:maxLen].decode('gbk').encode('utf8')
        except:
            try:
                s = string.decode('utf8').encode('gbk')[:maxLen - 1].decode('gbk').encode('utf8')
            except:
                pass
    return s


def center2(string, width, space = ' '):
    try:
        string.decode('utf8').encode('gbk')
    except:
        string = '编码错误'
    return string.decode('utf8').encode('gbk').center(width, space).decode('gbk').encode('utf8')


def main():
    initScreen()
    draw()
    restoreScreen()
    return 0


if __name__ =='__main__':
    try:
        main()
    except:
        restoreScreen()
        traceback.print_exc()


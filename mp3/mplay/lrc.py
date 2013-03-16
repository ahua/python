#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

def iconv(string):
    codings = ('utf8', 'gbk')
    for c in codings:
        error = False
        try:
            string.decode(c)
        except:
            error = True
        if not error:
            return string.decode(c).encode('utf8')
    return string


class Lrc:

    def __init__(self, lrc_filename):
        self.lrc_filename = lrc_filename
        self.tags = {"ti": '',   # title
                     "ar": '',   # artist
                     "al": '',   # album
                     "by": '',   # lrc author
                     "offset": 0 # ms
                     }
        self.lyrics = []  # (ts, line)
        self._load_lrc_file()
        
    def _get_ts(self, line):
        s = line.find("[") 
        e = line.find("]")
        t = line[s+1:e].split(":")
        line = line[e+1:]
        
        if len(t) != 2:
            return None, line
        
        if t[0] in ["ti", "ar", "al", "by"]:
            self.tags[t[0]] = t[1]
        elif t[0] == "offset":
            self.tags[t[0]] = int(t[1])
        else:
            try:
                m = int(t[0])
                s = float(t[1])
                return m*60*1000 + int(s*1000), line
            except:
                return None, line
        return None, line

    def _contain_meta(self, line):
        if line.find("[") >= 0 and line.find("]"):
            return True
        return False
    
    def _process(self, line):
        ts_list = []
        while self._contain_meta(line):
            ts, line = self._get_ts(line)
            if ts:
                ts_list.append(ts)
        for ts in ts_list:
            self.lyrics.append((ts, iconv(line)))

    
    def _load_lrc_file(self):
        if not os.path.exists(self.lrc_filename):
            return 
        
        with open(self.lrc_filename) as fp:
            for line in fp:
                self._process(line.strip().rstrip()) 
        self.lyrics.sort()               
            
        
    @classmethod
    def get_lrc_filename(cls, mp3_filename):
        if not os.path.exists(mp3_filename):
            return None
        return os.path.splitext(mp3_filename)[0] + ".lrc"
    
    def get_lyrics(self, ts, c=3):
        i = 0
        while i < len(self.lyrics) and self.lyrics[i][0] < ts:
            i = i + 1
        i = i - 1
        
        lyrics = {"lines": [],
                  "pos": -1}
        
        if i - c < 0:
            s = 0
            e = s + c*2 + 1
            p = i
        elif i + c >= len(self.lyrics):
            e = len(self.lyrics)
            s = e - c*2 - 1
            p = i - s 
        else:
            s = i - c
            e = i + c
            p = c 
        
        lyrics["lines"] = self.lyrics[s:e]
        lyrics["pos"] = p 
        
        return lyrics
    
if __name__ == "__main__":
    f = "/media/yhyan/backup/视频/Music/传奇.lrc"
    l = Lrc(f)
    for i in l.lyrics:
        print i[0], i[1]
    
    for i in l.get_lyrics(217700):
        print i
        
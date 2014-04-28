#coding:utf-8

import re, json, os, time
from redis import Redis
from datetime import datetime
from gnrl_base import GeneralBase
from app import App
from vod import Vod
from guide import Guide
from cat import Cat

class RtAgent(object):
    def __init__(self, conf):
        self.gb = GeneralBase(conf)
        self.app = App(conf)
        self.vod = Vod(conf)
        self.guide = Guide(conf)
        self.cat = Cat(conf)

    def interrupt(self):
        pass

    def accept(self, p, isnew = True):
        if p.get('_type') != 'normal':
            return

        if p.get('_device', '').lower() not in ['a11', 'a21', 'k72', 'k82', 'ud10a', 'ds70a', 'lx750a', 'lx755a', 'lx850a', 'lx960a', 'k91', 's31', 's51', 's61', 'e31', 'e62']:
            return

        if p.get('event') not in ['video_exit', 'app_start', 'launcher_vod_click', 'video_category_out']:
            return

        if isnew:
            if self.gb.run(p):
                self.app.run(p)
                self.vod.run(p)
                self.guide.run(p)
                self.cat.run(p)
        else:
            self.vod.run(p)

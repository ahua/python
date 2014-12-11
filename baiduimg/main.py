#!/usr/bin/env python
# -*- coding: utf-8 -*-

# */1 * * * * /home/yhyan/github/python/sinaspider/weibocn.py 2>&1 > /var/tmp/weibo/error.log

import json
import time
import urllib2
import urllib
import cookielib
import os
import datetime
import imghdr
from cStringIO import StringIO
from PIL import Image
 
class Fetcher(object):
    def __init__(self):
        self.cj = cookielib.LWPCookieJar()
        self.cookie_processor = urllib2.HTTPCookieProcessor(self.cj)
        self.opener = urllib2.build_opener(self.cookie_processor, urllib2.HTTPHandler)
        urllib2.install_opener(self.opener)
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                        'Referer':'','Content-Type':'application/x-www-form-urlencoded'}
     
    def get_rand(self, url):
        headers = {'User-Agent':'Mozilla/5.0 (Windows;U;Windows NT 5.1;zh-CN;rv:1.9.2.9)Gecko/20100824 Firefox/3.6.9',
                   'Referer':''}
        req = urllib2.Request(url ,urllib.urlencode({}), headers)
        resp = urllib2.urlopen(req)
        login_page = resp.read()
        rand = HTML.fromstring(login_page).xpath("//form/@action")[0]
        passwd = HTML.fromstring(login_page).xpath("//input[@type='password']/@name")[0]
        vk = HTML.fromstring(login_page).xpath("//input[@name='vk']/@value")[0]
        return rand, passwd, vk
     
    def login(self):
        url = 'http://image.baidu.com/'
        req = urllib2.Request(url, None, self.headers)
        resp = urllib2.urlopen(req)
        page = resp.read()
         
    def fetch(self, url, timeout=3):
        try:
            req = urllib2.Request(url, headers=self.headers)
            return urllib2.urlopen(req, timeout=timeout).read()
        except Exception as e:
            print e
            return None


def main(s, pn, idx):

    url = 'http://image.baidu.com/i?tn=resultjson_com&ipn=rj&ct=201326592&cl=2&lm=-1&st=-1&fm=star.index&fr=&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=gbk&word=%B6%AF%CE%EF&oq=%E5%8A%A8%E7%89%A9&rsp=-1&oe=utf-8&rn=60&step_word=&1245687482581.9358&397749115308.67426'
    url = url + '&pn=%s' % pn
    data = s.fetch(url)
    d = json.loads(data)

    urllist = []
    for i in d["data"]:
        urllist.append(i.get("thumbURL", None))

    for url in urllist:
        if not url:
            continue

        data = s.fetch(url)
        if not data:
            print url
            continue

        img = Image.open(StringIO(data))

        o_width, o_height = img.size
        if o_width >= o_height:
            left = (o_width - o_height)/2
            upper = 0
            right = left + o_height
            lower = upper + o_height
        else:
            left = 0
            upper = (o_height - o_width)/2
            right = left + o_width
            lower = upper + o_width
        n_img = img.crop([left, upper, right, lower])
        
        img_type = imghdr.what(StringIO(data))
        filename = '/tmp/img/%05d.%s' %(idx, img_type)
        n_img.save(filename, n_img.format)
        
        idx = idx + 1

if __name__ == "__main__":
    s = Fetcher()
    s.login()
    for pn in xrange(0, 2000, 60):
        try:
            main(s, pn, pn)
        except:
            pass





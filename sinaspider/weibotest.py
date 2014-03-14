#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import urllib2
import urllib
import cookielib
import os
import datetime
from bs4 import BeautifulSoup  # pip install beautifulsoup4 
import lxml.html as HTML
 
class Fetcher(object):
    def __init__(self, username=None, pwd=None, cookie_filename=None):
        self.cj = cookielib.LWPCookieJar()
        if cookie_filename is not None:
            self.cj.load(cookie_filename)
        self.cookie_processor = urllib2.HTTPCookieProcessor(self.cj)
        self.opener = urllib2.build_opener(self.cookie_processor, urllib2.HTTPHandler)
        urllib2.install_opener(self.opener)
         
        self.username = username
        self.pwd = pwd
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
     
    def login(self, username=None, pwd=None, cookie_filename=None):
        if self.username is None or self.pwd is None:
            self.username = username
            self.pwd = pwd
        assert self.username is not None and self.pwd is not None
         
        url = 'http://3g.sina.com.cn/prog/wapsite/sso/login.php?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F&backTitle=%D0%C2%C0%CB%CE%A2%B2%A9&vt='
        rand, passwd, vk = self.get_rand(url)
        data = urllib.urlencode({'mobile': self.username,
                                 passwd: self.pwd,
                                 'remember': 'on',
                                 'backURL': 'http://weibo.cn/',
                                 'backTitle': '新浪微博',
                                 'vk': vk,
                                 'submit': '登录',
                                 'encoding': 'utf-8'})
        url = 'http://3g.sina.com.cn/prog/wapsite/sso/' + rand
        req = urllib2.Request(url, data, self.headers)
        resp = urllib2.urlopen(req)
        page = resp.read()
        link = HTML.fromstring(page).xpath("//a/@href")[0]
        if not link.startswith('http://'): link = 'http://weibo.cn/%s' % link
        req = urllib2.Request(link, headers=self.headers)
        urllib2.urlopen(req)
        if cookie_filename is not None:
            self.cj.save(filename=cookie_filename)
        elif self.cj.filename is not None:
            self.cj.save()
        else:
            self.cj.filename = "/tmp/cookie.txt"
            self.cj.save()

        #print 'login success!'
         
    def fetch(self, url):
        #print 'fetch url: ', url
        req = urllib2.Request(url, headers=self.headers)
        return urllib2.urlopen(req).read()


def main(weibo_addr="http://weibo.cn/u/1738850664"):
    start = datetime.datetime.now()
    
    s = Fetcher('yanjiahua90@163.com', 'yanyahuapassword')
    s.login()
    
    text = s.fetch(weibo_addr)
    soup = BeautifulSoup(text)
    
    name = soup.find("span", {"class": "ctt"}).getText().split()[0]
    tip2 = soup.find("div", {"class": "tip2"}).getText().split()
    
    end = datetime.datetime.now()
    
    m = start.strftime("%Y%m%d_%H_%M_%S")
  
    li = "%s %s %s %s %s\n" % (m, name, tip2[0], tip2[1], tip2[2])
    print li,

while True:
    main()
    time.sleep(30)


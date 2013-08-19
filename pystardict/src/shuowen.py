#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup  # pip install beautifulsoup4


URL_FORMAT = "http://www.shuowen.org/view/%s"

def get_word(i):
    url = URL_FORMAT % i
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)

    vol, radical = [i.text for i in\
                    soup.find("div", {"class": "span6"}).findAll("a")]
    data = []


for i in range(1, 9834):
    data = get_word(i)

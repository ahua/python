#!/usr/bin/env python

import sys
import datetime
import simplejson
import urllib2
import MySQLdb
from bs4 import BeautifulSoup  # pip install beautifulsoup4

def get_soup(url):
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    return soup

def get_content(href):
    soup = get_soup(href)
    div =  soup.find("div", {"id": "intro"})
    td_list = div.find("table").find_all("td")

    s = []
    ntd_list = [td_list[1], td_list[45], td_list[47]]
    for td in ntd_list:
        s.append(td.text.encode("utf8"))
    return s

def get_data(stockid):
    href = "http://cj.gw.com.cn/news/stock/%s/gsjs.shtml" % stockid
    return get_content(href)


DB = None
C = None


def init_db(user, passwd, db, host="112.124.39.18", charset="utf8"):
    global DB, C

    DB = MySQLdb.connect(user=user, passwd=passwd, db=db, host=host, charset=charset)
    C = DB.cursor()


def close_db():
    global DB, C

    C.close()
    DB.close()


USER = "yhyan"
PASSWD = "yhyanP@55word"
DB = "dosite"


def get_stocklist():
    stocklist = []
    with open("id_name.txt") as fp:
        for li in fp:
            sid, sname = li.rstrip().split("\t")
            if sid[0] == "0" or sid[0] == "3":
                stocklist.append(["sz" + sid, sname])
            else:
                stocklist.append(["sh" + sid, sname])
    return stocklist[1:]

if __name__ == "__main__":
    stocklist = get_stocklist()
    for sid, sname in stocklist:
        data = get_data(sid)
        res = [sid, sname] + data
        print " ".join(res)
            
            



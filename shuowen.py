#!/usr/bin/env python
# -*- coding: utf-8 -*-
from decimal import Decimal
import datetime
import urllib2
from bs4 import BeautifulSoup  # pip install beautifulsoup4
import MySQLdb
import sys

DB = None
C = None

def init_db(user, passwd, db, host="localhost", charset="utf8"):
    global DB, C

    DB = MySQLdb.connect(user=user, passwd=passwd, db=db, host=host, charset=charset)
    C = DB.cursor()

def close_db():
    global DB, C

    C.close()
    DB.close()

def insert(data):
    global DB, C
    sql = """insert into dic_shuowen(idx, juanshu, bushou, pinyin, qieyin, word, body) values (%s, '%s', '%s', '%s', '%s', '%s', '%s')""" %  tuple(data)
    #C.executemany(sql, data)
    C.execute(sql)
    DB.commit()




def shuowen(i):
    url = "http://www.shuowen.org/view/%s" % i
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)

    d = soup.find("div", class_="span6").find_all('a')
    juanshu = d[0].getText()
    bushou = d[1].getText()
    
    d = soup.find("div", class_="span6 text-right")
    t = d.getText().split()
    pinyin = t[0]
    qieyin = t[2]

    word = soup.find("span", class_="media-object pull-left").getText().strip().rstrip()
    body = soup.find("div", class_="media-body").getText().strip().rstrip()
    
    return [i, juanshu, bushou, pinyin, qieyin, word, body]

if __name__ == "__main__":
    USER = "yhyan"
    PASSWD = "yhyanP@55word"
    DB = "dosite"
    HOST = "112.124.39.18"
    init_db(USER, PASSWD, DB, HOST)
    for i in range(2116, 9834):
        try:
            data = shuowen(i)
            insert(data)
        except:
            pass

    close_db()


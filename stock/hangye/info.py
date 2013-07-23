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
    sql = """insert into st_info(stockid, tradecode, name) values (%s, %s, %s)"""
    C.executemany(sql, data)
    DB.commit()


def main(filepath, tradecode):
    f = open(filepath)
    lines = f.readlines()
    f.close()
    
    data = []
    for l in lines:
        values = l.split("\t")
        if len(values) != 13:
            continue
        stockid = Decimal(values[0][2:])
        name = values[1].decode("utf-8")
        data.append([stockid, tradecode, name])
    
    insert(data)
#    print data


if __name__ == "__main__":
    USER = "yhyan"
    PASSWD = "yhyanP@55word"
    DB = "dosite"
    HOST = "112.124.39.18"
    init_db(USER, PASSWD, DB, HOST)
    main(sys.argv[1], sys.argv[1])
    close_db()


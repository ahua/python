#!/usr/bin/env python

from decimal import Decimal
import datetime
import urllib2
from bs4 import BeautifulSoup  # pip install beautifulsoup4
import MySQLdb
import sys


DB = None
C = None

def init_db(user, passwd, db, host="localhost"):
    global DB, C

    DB = MySQLdb.connect(user=user, passwd=passwd, db=db, host=host)
    C = DB.cursor()

def insertmany(tuple_list):
    global DB, C
    C.executemany(
        """INSERT INTO st_info (stockid, hyid)
        VALUES (%s, %s)""",
        tuple_list)
    DB.commit()  # this line is important.

def get_stockid_list(filepath):
    l = []
    with open(filepath) as fp:
        for li in fp:
            l.append(li.split("\t")[0][2:])
    return l


if __name__ == "__main__":
    init_db("yhyan", "yhyanP@55word", "dosite")

    stockid_list = get_stockid_list(sys.argv[1])
    tuple_list = [(i, sys.argv[1]) for i in stockid_list]

    insertmany(tuple_list)



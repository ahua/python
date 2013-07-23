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
        """INSERT INTO st_daily
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        on duplicate key update y_close = %s""",
        tuple_list)
    DB.commit()  # this line is important.

def update(stockid):
    global DB, C

    C.execute("SELECT * FROM st_daily WHERE stockid = %s ORDER BY `day`" % stockid)
    objs = C.fetchall()
    c = len(objs)
    data = []
    y_close_list = []
    for i in range(0, c):
        t0 = list(objs[0]) if i == 0 else list(objs[i-1])
        t1 = list(objs[i])
        data.append(t1 + [t0[7]])

    insertmany(data)


def get_stockid_list():
    return [600230]
    global DB, C
    C.execute("""select distinct stockid from st_daily""")
    objs = C.fetchall()
    return [o[0] for o in objs]

    
if __name__ == "__main__":
    init_db("yhyan", "yhyanP@55word", "dosite")

    stockid_list = get_stockid_list()
    for stockid in stockid_list:
        update(stockid)


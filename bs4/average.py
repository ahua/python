#!/usr/bin/env python

import datetime
from decimal import Decimal
import MySQLdb
from operator import itemgetter


DB = None
C = None

def init_db(user, passwd, db, host="localhost"):
    global DB, C

    DB = MySQLdb.connect(user=user, passwd=passwd, db=db, host=host)
    C = DB.cursor()

def close_db():
    global DB, C

    C.close()
    DB.close()


def get_all_average():
    sql = "SELECT stockid, SUM(average)/COUNT(*) FROM st_daily GROUP BY stockid;"
    C.execute(sql)
    l = C.fetchall()
    d = {}
    for k, v in l:
        d.update({k:v})
    return d


def get_all_price(someday):
    sql = """SELECT stockid, close FROM st_daily WHERE `day` = DATE("%s")"""
    C.execute(sql % someday.strftime("%Y-%m-%d"))
    l = C.fetchall()
    d = {}
    for k, v in l:
        d.update({k:v})
    return d


def main(someday):
    avgs = get_all_average()
    prices = get_all_price(someday)
    rates = {}
    for stockid, price in prices.iteritems():
        average = avgs[stockid]
        rate = (price - average) / average
        rates.update({stockid:rate})
    sorted_rates = sorted(rates.iteritems(), key=itemgetter(1), reverse=True)
    for i in sorted_rates:
        print i


if __name__ == "__main__":
    USER = "yhyan"
    PASSWD = "yhyanP@55word"
    DB = "dosite"

    init_db(USER, PASSWD, DB)
    main(datetime.datetime(2013, 07, 11))
    close_db()


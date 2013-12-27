#!/usr/bin/env python

import sys
import datetime
import simplejson
import urllib2
import MySQLdb
from bs4 import BeautifulSoup  # pip install beautifulsoup4
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

URL_FORMAT = "http://cctv.cntv.cn/lm/xinwenlianbo/%s.shtml"

browser = None

def get_data(code):
    global browser
    if not browser:
        browser = webdriver.Firefox()

    URL_FORMAT = "http://cj.gw.com.cn/news/stock/%s/cpbd.shtml"
    url = URL_FORMAT % code
    browser.get(url)

    jzrq = browser.find_element_by_id("jzrq").text
    zgb = browser.find_element_by_id("zgb").text  # zong gu ben 
    mgsy = browser.find_element_by_id("mgsy").text   # mei gu shouyi 
    ssrq = browser.find_element_by_id("ssrq").text   # shangshi shijian
    mqlt = browser.find_element_by_id("mqlt").text   # liu tong a gu 
    mgjzc = browser.find_element_by_id("mgjzc").text  # mei gu jin zhi chang
    mgjyxjl = browser.find_element_by_id("mgjyxjl").text # mei gu xianjinliu
    mggjj = browser.find_element_by_id("mggjj").text  # mg gongjijing
    jzcsyl = browser.find_element_by_id("jzcsyl").text  # jzc shouyilv
    jlrtbzz = browser.find_element_by_id("jlrtbzz").text  # jlirun shouyilu
    mgwfplr = browser.find_element_by_id("mgwfplr").text  # meigu wei feipei lrun
    zysrtbzz = browser.find_element_by_id("zysrtbzz").text  # zhuyinshouru

    sql = """update StockTradeRecord_stock set update_date = '%s', total_capital = %s, eps = %s, market_date = '%s', outstanding_capital = %s, 
            bvps = %s , cfps = %s, afps = %s , roe = %s, npgr = %s, upps = %s, mbrg = %s
           where code = '%s';""" % (jzrq, zgb, mgsy, ssrq, mqlt, mgjzc, mgjyxjl, mggjj, jzcsyl, jlrtbzz, mgwfplr, zysrtbzz, code)
    print sql

    data = []
    return data

DB = None
C = None

def get_stockcode_list():
    global C

    C.execute("""select code from StockTradeRecord_stock""")
    objs = C.fetchall()
    return [o[0] for o in objs]


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

if __name__ == "__main__":
    init_db(USER, PASSWD, DB)
    stockcode_list = get_stockcode_list()
    for code in stockcode_list:
        if code == "sh000001":
            continue
        get_data(code)
    close_db()


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

S_TAG = '<div class="body" id="content_body">'
E_TAG = '</div>'

def get_soup(url):
    html = urllib2.urlopen(url).read()
    s = html.find(S_TAG)
    if s < 0:
        return None
    e = html.find(E_TAG, s)
    content = html[s:e+len(E_TAG)]
    soup = BeautifulSoup(content)
    return soup

def get_content(href):
    soup = get_soup(href)
    if not soup:
        return ""
    plist = soup.find_all("p")
    s = ""
    for p in plist:
        s += p.text
    return s

def get_data_by_day(someday):
    global browser
    if not browser:
        browser = webdriver.Firefox()

    url = URL_FORMAT % someday.strftime("%Y%m%d")
    browser.get(url)

    div = None
    try:
        div = browser.find_element_by_id("title_01")
    except NoSuchElementException:
        try:
            div = browser.find_element_by_id("SUBD1368521784291372")
        except:
            print "Not find table: %s" % someday.strftime("%Y%m%d")
            return []

    a_list = div.find_elements_by_tag_name("a")
    data = []
    num = 0
    for a in a_list:
        href = a.get_attribute("href")
        title = a.text.encode("utf8")
        #content = get_content(href)
        #content = ""
        print title
        print href
        #print content
        data.append([num, someday, href, title, datetime.datetime.now()])
        num = num + 1
    return data


def insert_to_db(iterdata):
    global DB, C

    sql = """INSERT INTO  news_xwlb (`num`, `day`, `url`, `title`, created_at)
           VALUES (%s, %s, %s, %s, %s)
            on duplicate key update updated_at = now()"""
    C.executemany(sql, iterdata)
    DB.commit()  # this line is important.


def get_daylist(startday, endday):
    daylist = []
    while startday <= endday:
        daylist.append(startday)
        startday = startday + datetime.timedelta(days=1)
    return daylist


def main(someday):
    data = get_data_by_day(someday)
    insert_to_db(data)


DB = None
C = None


def init_db(user, passwd, db, host="******", charset="utf8"):
    global DB, C

    DB = MySQLdb.connect(user=user, passwd=passwd, db=db, host=host, charset=charset)
    C = DB.cursor()


def close_db():
    global DB, C

    C.close()
    DB.close()


USER = "***"
PASSWD = "****"
DB = "dosite"


if __name__ == "__main__":
    if len(sys.argv) == 2:
        someday = datetime.datetime.strptime(sys.argv[1], "%Y%m%d")
        daylist = [someday]
    elif len(sys.argv) == 3:
        startday = datetime.datetime.strptime(sys.argv[1], "%Y%m%d")
        endday = datetime.datetime.strptime(sys.argv[2], "%Y%m%d")
        daylist = get_daylist(startday, endday)
    else:
        someday = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        daylist = [someday]

    init_db(USER, PASSWD, DB)
    for someday in daylist:
        main(someday)
    close_db()


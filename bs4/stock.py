#!/usr/bin/env python

from decimal import Decimal
import datetime
import urllib2
from bs4 import BeautifulSoup  # pip install beautifulsoup4
import MySQLdb

DB = None
C = None

URL_FORMAT = "http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/%06d.phtml?year=%s&jidu=%s"

JIDU = {
  1:1, 2:1, 3:1,
  4:2, 5:2, 6:2,
  7:3, 8:3, 9:3,
  10:4, 11:4, 12:4
}


def get_data_by_jidu(year, jidu, stockid):
    url = URL_FORMAT % (stockid, year, jidu)
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    table = soup.find(id="FundHoldSharesTable")
    if not table:
        return []
    tr_list = table.find_all("tr")
    if not tr_list or len(tr_list) <= 2:
        return []
    
    data = []
    for tr in tr_list[2:]:
        l = tr.text.split() # day, open, high, low, close, turnover, money
        if len(l) != 7:
            continue
        average = (Decimal(l[1]) + Decimal(l[2]) + Decimal(l[3]) + Decimal(l[4]))/4
        data.append([stockid] + l + [datetime.datetime.now(), average])
    return data


def get_data_by_day(someday, stockid):
    year = someday.year
    jidu = JIDU[someday.month]

    data = get_data_by_jidu(year, jidu, stockid)
    day_str = someday.strftime("%Y-%m-%d")

    for i in data:
        if i[1] == day_str:
            return [i]

    return []


ONE_DAY = datetime.timedelta(days=1)

def get_next_yj(y, j):
    if j == 4:
        return (y + 1, 1)
    return (y, j+1)

def get_yjlist(startday, endday):
    yjlist = []
    
    s_y, s_j = startday.year, JIDU[startday.month]
    e_y, e_j = get_next_yj(endday.year, JIDU[endday.month])
    
    while (s_y, s_j) != (e_y, e_j):
        yjlist.append((s_y, s_j))
        s_y, s_j = get_next_yj(s_y, s_j)

    return yjlist


def get_date_by_range(startday, endday, stockid):
    d = []
    startday_str = startday.strftime("%Y-%m-%d")
    endday_str = endday.strftime("%Y-%m-%d")
    yjlist = get_yjlist(startday, endday)


    for y, j in yjlist:
        t = get_data_by_jidu(y, j, stockid)
        for i in t:            
            if i[1] >= startday_str and i[1] <= endday_str:
                d.append(i)
    return d


def insertmany(tuple_list):
    global DB, C
    C.executemany(
        """INSERT INTO st_daily (stockid, day, open, high, low, close, turnover, money, created_at, average)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        tuple_list)
    DB.commit()  # this line is important.


def get_stockid_list():
    global C

    C.execute("""select distinct stockid from st_daily""")
    objs = C.fetchall()
    return [o[0] for o in objs]


def get_latest_day(stockid):
    global C

    C.execute("SELECT `day` FROM st_daily WHERE stockid = %s ORDER BY `day` DESC LIMIT 1" % stockid)
    o = C.fetchone()
    if not o:
        return None
    return o[0]

def update_to_now(stockid):
    latest_day = get_latest_day(stockid)
    if not latest_day:
        return False
    startday = latest_day + ONE_DAY
    endday = datetime.datetime.now()
    
    data = get_date_by_range(startday, endday, stockid)
    print "Start insertmany stockid = %s, startday = %s, endday = %s" % (stockid, startday, endday)
    insertmany(data)
    print "Finish insertmany stockid = %s, startday = %s, endday = %s" % (stockid, startday, endday)
    return True


def update_all_to_now():
    stockid_list = get_stockid_list()
    for stockid in stockid_list:
        update_to_now(stockid)


def init_db(user, passwd, db, host="localhost"):
    global DB, C

    DB = MySQLdb.connect(user=user, passwd=passwd, db=db, host=host)
    C = DB.cursor()

def close_db():
    global DB, C

    C.close()
    DB.close()


def main():
    update_all_to_now()

if __name__ == "__main__":
    USER = "yhyan"
    PASSWD = "yhyanP@55word"
    DB = "dosite"

    init_db(USER, PASSWD, DB)
    main()
    close_db()


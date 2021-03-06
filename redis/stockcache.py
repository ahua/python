#!/usr/bin/env python
import urllib2
import datetime
import redis
import pickle
import MySQLdb

class StockdataCache():
    _expire_time = 10 * 60
    _r = None
    def __init__(self, host='localhost', port=6379, db=0):
        pool = redis.ConnectionPool(host=host, port=port, db=db)
        self._r = redis.Redis(connection_pool=pool)
        self._r.ping()
        
    def set_expire_time(self, expire_time):
        self.expire_time = expire_time
    
    def set(self, code, data):
        if not self.exists(code):
            self._r.set(code, data)
            
            t = datetime.datetime.now()
            m = t.hour * 60 + t.minute
            if m >= 570 and m <= 900:
                self._r.expire(code, int(self.expire_time))
            else:
                s = datetime.datetime(1992, 8, 14, t.hour - 15, t.minute, t.second)
                e = datetime.datetime(1992, 8, 14, 18, t.minute, t.second)
                self._r.expire(code, int((e-s).total_seconds()))
            return True
        return False

    def exists(self, code):
        return self._r.exists(code)

    def get(self, code):
        if self._r.exists(code):
            return pickle.loads(self._r.get(code))
        else:
            url = "http://qt.gtimg.cn/?q=%s" % code
            c = urllib2.urlopen(url).read()
            l = c.split("~")
            data = [l[3], l[32], l[39], l[44], l[45]]
            self.set(code, pickle.dumps(data))
            return data

cache = StockdataCache(host="112.124.39.18")
def get_stock_data(code):
    return cache.get(code)

DB = None
C = None
def init_db(user="yhyan", passwd="yhyanP@55word", db="dosite", host="112.124.39.18"):
    global DB, C
    DB = MySQLdb.connect(user=user, passwd=passwd, db=db, host=host)
    C = DB.cursor()

def close_db():
    global DB, C
    C.close()
    DB.close()

def get_stockcode_list():
    global C

    C.execute("""select code from StockTradeRecord_stock""")
    objs = C.fetchall()
    return [o[0] for o in objs]


if __name__ == "__main__":
    init_db()
    codelist = get_stockcode_list()
    for code in codelist:
        print code
        print get_stock_data(code)


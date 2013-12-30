#!/usr/bin/env python
import urllib2
import datetime
import redis
import pickle
import MySQLdb

class StockdataCache():
    _expire_time = 10 * 60
    _r = None
    DB = None
    C = None

    def __init__(self, host='localhost', port=6379, db=0):
        pool = redis.ConnectionPool(host=host, port=port, db=db)
        self._r = redis.Redis(connection_pool=pool)
        self._r.ping()
        self.init_db()
        
    def init_db(self, user="yhyan", passwd="yhyanP@55word", db="dosite", host="112.124.39.18"):
        self.DB = MySQLdb.connect(user=user, passwd=passwd, db=db, host=host)
        self.C = self.DB.cursor()

    def close_db(self):
        self.C.close()
        self.DB.close()

    def get_stockcode_list(self):
        self.C.execute("""select code from StockTradeRecord_stock""")
        objs = self.C.fetchall()
        return [o[0] for o in objs]

    def set_expire_time(self, expire_time):
        self.expire_time = expire_time
    
    def set(self, code, data):
        if not self.exists(code):
            self._r.set(code, pickle.dumps(data))
            self._r.expire(code, 30)
            return True
        return False

    def exists(self, code):
        return self._r.exists(code)

    def get_from_mysql(self, code):
        self.C.execute("""select price, incrate, pe, ltsz, total_value from StockTradeRecord_stockvalue where code = '%s'""" % code)
        objs = self.C.fetchall()
        return o[0]

    def save_to_mysql(self, code, data):
        sql = """update StockTradeRecord_stockvalue set price = %s, incrate = %s, pe =%s, ltsz = %s, total_value =%s where code = '%s'; """ 
        #self.C.execute(sql, (data[0], data[1], data[2], data[3], data[4], code))
        print sql % (data[0], data[1], data[2], data[3], data[4], code)

    def get(self, code):
        if self._r.exists(code):
            return pickle.loads(self._r.get(code))
        else:
            return self.get_from_mysql(code)


cache = StockdataCache()
def get_stock_data(code):
    return cache.get(code)

def try_to_float(s):
    try:
        return float(s)
    except:
        return 0

def parse_stock_data(code):
    url = "http://qt.gtimg.cn/?q=%s" % code
    c = urllib2.urlopen(url).read()
    l = c.split("~")
    data = [l[3], l[32], l[39], l[44], l[45]]
    data = [try_to_float(i) for i in data]
    return data

if __name__ == "__main__":
    codelist = cache.get_stockcode_list()
    for code in codelist:
#        print code
        data = parse_stock_data(code)
        cache.save_to_mysql(code, data)



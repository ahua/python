#!/usr/bin/env python

import MySQLdb

_db = None
_c = None

def connect(user, host, passwd, db, port=3306):
    global _db
    
    if not _db:
        try:
            _db = MySQLdb.connect(user=user,
                                 host=host,
                                 passwd=passwd,
                                 db=db,
                                 port=port)
            _c = _db.cursor()
        except Exception, e:
            print e
            return False
    return True


def close():
    global _db, _c
    if _c: _c.close()
    if _db: _db.close()
    _c = None
    _db = None


# c.fetchone()
# c.fetchmany(n)
# c.fetchall()
# c.execute()
# c.executemany(
#      """INSERT INTO breakfast (name, spam, eggs, sausage, price)
#      VALUES (%s, %s, %s, %s, %s)""",
#      [
#      ("Spam and Sausage Lover's Plate", 5, 1, 8, 7.95 ),
#      ("Not So Much Spam Plate", 3, 2, 0, 3.95 ),
#      ("Don't Wany ANY SPAM! Plate", 0, 4, 3, 5.95 )
#      ] )
       

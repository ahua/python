#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
from pystardict import Dictionary


def get_dic_list(dicpath):
    d = Dictionary(dicpath)
    res = []
    for k in d.idx.iterkeys():
        res.append(["".join(k), d[k]])
    return res


database = None
cursor = None

USER = "yhyan"
PASSWD = "yhyanP@55word"
DB = "dosite"


def init_db(user=USER, passwd=PASSWD, db=DB, host="10.2.101.97"):
    global database, cursor
    database = MySQLdb.connect(user=user,
                               passwd=passwd,
                               db=db,
                               host=host,
                               charset="utf8")
    cursor = database.cursor()


def close_db():
    global database, cursor
    cursor.close()
    database.close()


def insertmany(table, tuple_list):
    global database, cursor
    sql = "INSERT INTO dic_%s (word, content) VALUES (%%s, %%s)" % table
    cursor.executemany(sql, tuple_list)
    database.commit()  # this line is important.

def create_table(table):
    sql = """drop table if exists dic_%s;
          CREATE TABLE `dic_%s` (
              `id` int(11) NOT NULL AUTO_INCREMENT,
              `word` varchar(255) DEFAULT NULL,
              `content` text,
              PRIMARY KEY (`id`)
          ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
         """ % (table, table)
    print sql

table_list = [#"xiandaihanyucidian_fix",
              #"rcc",
              #"ree",
              "lazyworm_ec",
              "lazyworm_ce",
              #"hycihai",
              #"hanyudacidian",
              #"ghycyz",
              #"gaojihanyudacidian_fix",
              "21shijishuangxiangcidian"]

init_db()
for table in table_list:
    #create_table(table)
    dic_list = get_dic_list("/var/tmp/startdict/dic/" + table)
    insertmany(table, dic_list)
    print "Finished", table
close_db()
print "finished"

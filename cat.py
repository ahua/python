#coding:utf-8

import re, json, os, time, threading
from datetime import datetime
from redis import Redis
from rt_mysql import MysqlConn 
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Cat(MysqlConn):
    def __init__(self, conf):
        MysqlConn.__init__(self, conf)
        self.r = Redis(host = conf.get('redis_mysql', 'ip'),
                       port = conf.get('redis_mysql', 'port', int),
                       db = conf.get('redis_mysql', 'db', int))

        self.c_type_2id  = 'pink_general_device_type_2id'
        self.c_dev_2id   = 'pink_general_device_2id'
        self.conf  = conf
        self.__init_table()
        self.count = 0
        
    def __init_table(self):
        mysql = self.get_conn()
        cur = mysql.cursor()
        cur.execute("show tables;")
        exist_tables = []
        for line in cur.fetchall():
            exist_tables.append(line[0])

        if 'video_category_out' not in exist_tables:
            sql = """create table video_category_out(
                          id int unsigned not null auto_increment,
                          time timestamp,
                          sn int unsigned,
                          device smallint unsigned,
                          title varchar(512),
                          section varchar(512),
                          position smallint,
                          to_title varchar(512),
                          to_item int unsigned,
                          primary key(`id`)
                        );"""
            cur.execute(sql)

        mysql.close()
        print "video_category_out table init done"

    def run(self, p):
        if p.get('event') != 'video_category_out':
            return

        time_s= p.get('time')
        sn    = p.get('sn').strip().lower()
        device= p.get('_device').strip().lower()
        title = p.get("title")
        section = p.get("section")
        position = p.get("position")
        to_title = p.get("to_title")
        to_item = p.get("to_item")
        
        if not time_s or not sn:
            return

        sql = """insert ignore into
                    video_category_out(time, sn, device, title, section, position, to_title, to_item)
                    values('%s', %s, %s, %s)
                 """ % (time_s, self.r.hget(self.c_dev_2id, sn), self.r.hget(self.c_type_2id, device),
                        title, section, position, to_title, to_item)
        self.insert_sql(sql)

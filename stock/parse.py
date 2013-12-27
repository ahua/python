#!/usr/bin/env python
#-*- coding:utf8 -*-
fp = open("stocklist.txt", "r")
# 代码 名称 现价 涨跌 涨幅% 今开 最高 最低 昨收 市盈(动) 总金额 量比 换手% 地区 细分行业 流通股本 流通市值 财务更新 净资产 资产负债率% 流动资产 固定资产

NUM2ID = {"0":"sz", "3": "sz", "6": "sh"}

stock = []
for li in fp:
    if li.startswith("#"):
        continue
    d = {}
    t = li.split("\t")
    
    try:
        d["code"] = NUM2ID[t[0][0]] + t[0]
        d["name"] = t[1]
        d["region"] = t[13]
        d["industry"] = t[14]
        stock.append(d)
    except:
        print t[0], t[1]

for i in stock:
#    sql_format = '''update StockTradeRecord_stock set name = "%s" where id = getstockid("%s");''' % (i["name"], i["code"])
#    print sql_format

    sql_format = '''update StockTradeRecord_stock set industry_id = getindustryid("%s") where id = getstockid("%s");'''
    print sql_format %(i["industry"], i["code"])
        
    sql_format = '''update StockTradeRecord_stock set region_id = getregionid("%s") where id = getstockid("%s");'''
    print sql_format %(i["region"], i["code"])
        
def insert_tosock():
    stock_id = 2
    for i in stock:
        sql_format = """insert into StockTradeRecord_stock(code, name, industry_id, region_id) values('%s', '%s', 1, 1);"""
        sql = sql_format % (i["code"], i["name"])
        print sql
        sql = """insert into StockTradeRecord_stock_tags(stock_id, tag_id) values(%s, 1);""" % stock_id
        print sql
        stock_id = stock_id + 1

#insert_tosock()


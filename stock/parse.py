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
    t = li.split()
    
    try:
        d["code"] = NUM2ID[t[0][0]] + t[0]
        d["name"] = t[1]
        
        stock.append(d)
    except:
        print t[0], t[1]


for i in stock:
    sql_format = """insert into StockTradeRecord_stock(code, name, tag_id, industry_id, region_id, concept_id) values('%s', '%s', 1, 1, 1, 1);"""
    sql = sql_format % (i["code"], i["name"])
    print sql


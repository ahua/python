#!/usr/bin/env python

import sys

tag_id = 4
fp = open(sys.argv[1])
codelist = []
for li in fp:
    v = li.split()
    if v[0][0] == "0":
        codelist.append("sz" + v[0])
    if v[0][0] == "3":
        codelist.append("sz" + v[0])
    if v[0][0] == "6":
        codelist.append("sh" + v[0])

sql_format = '''insert into StockTradeRecord_stock_tags(stock_id, tag_id) values (getstockid("%s"), %s);'''

for code in codelist:
    print sql_format % (code, tag_id)

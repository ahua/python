'''
Created on Jun 3, 2013

@author: yhyan
'''

import csv
import cPickle as pickle

outputfilename = "/tmp/t.csv"
with open(outputfilename, 'wb') as out:
    writer = csv.writer(out, delimiter='\t')
    writer.writerow(['20120305', 'xxxxx', 'hell""', "0"])
    writer.writerow(['20120306', 'yyyyy', pickle.dumps("yes"), "1"])

with open(outputfilename, "rb") as fin:
    reader = csv.reader(fin, delimiter="\t")
    t = 3 + 5

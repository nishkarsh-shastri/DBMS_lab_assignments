__author__ = 'nishkarsh'
#!/usr/bin/python

import sys
import MySQLdb as mdb
from time import sleep
import time
from sys import argv
import networkx as nx

con = mdb.connect('10.5.18.66', '12CS10034', 'btech12', '12CS10034')
cur = con.cursor()

def findAnswer():
    sql = "create or replace view vcast as select mid,pid from 12CS10034_Movie Natural Join 12CS10034_M_Cast"
    cur.execute(sql)

    sql = "select distinct A.mid,B.mid from vcast A,vcast B where A.pid = B.pid and A.mid>B.mid"
    cur.execute(sql)

    M = nx.Graph()

    count = 0
    for x in cur.fetchall():
        i = -1
        old = ""
        v1 = ""
        v2 = ""
        for y in x:
            i=i+1
            if(i==0):
                v1=y
            elif(i==1):
                v2=y
                i=-1
        M.add_edge(v1,v2)
        M.add_edge(v2,v1)

    x = nx.graph_clique_number(M)
    print "The size of largest mutually similar group is: ",x


if __name__ == "__main__":
    findAnswer()
__author__ = 'nishkarsh'

import operator
import sys
import MySQLdb as mdb
from time import sleep
import time
from sys import argv
import networkx as nx

con = mdb.connect('10.5.18.66', '12CS10034', 'btech12', '12CS10034')
cur = con.cursor()

def findAnswer():
    sql = "select * from 12CS10034_orderedSeparation"
    cur.execute(sql)
    #get values from the table created in previous parts and then create a new table outputting the values.
    for y in cur.fetchall():
        if y[2] != -1:
            sql = "INSERT INTO 12CS10034_canfind VALUES('"+y[0]+"','"+y[1]+"','YES')"
            cur.execute(sql)
        else:
             sql = "INSERT INTO 12CS10034_canfind VALUES('"+y[0]+"','"+y[1]+"','NO')"
             cur.execute(sql)

    con.commit()

if __name__ == "__main__":

    #sql = "CREATE TABLE IF NOT EXISTS 12CS10034_canfind(pid1 VARCHAR(9),firstName VARCHAR(50),pid2 VARCHAR(9),secondName VARCHAR(50),answer varchar(6),constraint primary key(pid1,pid2))"
    sql = "CREATE TABLE IF NOT EXISTS 12CS10034_canfind(firstName VARCHAR(50),secondName VARCHAR(50),answer varchar(6))" # again the problem of primary key persists. Its better to use above table.
    cur.execute(sql)
    findAnswer()

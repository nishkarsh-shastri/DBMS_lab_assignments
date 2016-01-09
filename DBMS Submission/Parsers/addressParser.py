__author__ = 'nishkarsh'
import sys
from sys import argv
import MySQLdb as mdb

con = mdb.connect('localhost', 'root', 'madeforyou', 'election')
cur = con.cursor()



# CREATE TABLE District_Constituency
# (
# 	District VARCHAR(20),
# 	Acno Char(10),
# 	PRIMARY KEY(District,Acno),
# 	FOREIGN KEY dc_fk(Acno) REFERENCES Constituency(Acno)
# # )
# -- Constituency
# CREATE TABLE Constituency (
# Acno Char(10),
# Acname VARCHAR(30) NOT NULL,
# Population INT,
# PCno VARCHAR(10),
# PRIMARY KEY c_pk (Acno),
# CONSTRAINT FOREIGN KEY c_fk(PCno) REFERENCES Parliamentary_Constituency(PCno));
#
# CREATE TABLE Address (
# PIN INT NOT NULL,
# PO VARCHAR(20) NOT NULL,
# Town VARCHAR(50) NOT NULL,
# District VARCHAR(50) NOT NULL,
# State VARCHAR(50) NOT NULL,
# Acno Char(10),
# PRIMARY KEY ad_pk (town,PIN),
# FOREIGN KEY ad_fk(Acno) REFERENCES Constituency(Acno));


def encode(c):
	s = str(c)
	for i in range(0,(6-len(s))):
		s = "0"+s

	return s





if __name__ == "__main__" :
   f = open(argv[1],'r')
   lines = f.read().splitlines()
   for item in lines:
        s = item.split(',')
        sql = "select Acno from Address where Town='"+s[0].replace("\'","\'\'")+"' limit 1"
        print sql
        cur.execute(sql)
        res = cur.fetchone()
        print res
        if(res==None):
                sql = "select Acno from District_Constituency where District='"+s[3]+"' order by rand() limit 1"
                print sql
                cur.execute(sql)
                res = cur.fetchone()
                acno = res[0]
                print "rand "+acno
        else:
                acno = res[0]
                print "found" + acno

        sql = "INSERT INTO Address VALUES('"+s[1]+"','"+s[0].replace("\'","\'\'")+"','"+s[0].replace("\'","\'\'")+"','"+s[3]+"','"+s[2]+"','"+acno+"')"
        print sql
        cur.execute(sql)
        con.commit()


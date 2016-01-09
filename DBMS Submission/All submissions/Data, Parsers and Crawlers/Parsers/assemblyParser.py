import sys
from sys import argv
import MySQLdb as mdb

con = mdb.connect('localhost', 'root', 'madeforyou', 'election')
cur = con.cursor()


# CREATE TABLE Parliamentary_Constituency
# (
# 	PCno VARCHAR(10),
# 	PCName VARCHAR(30) NOT NULL,
# 	State VARCHAR(25) NOT NULL,
# 	PRIMARY KEY(PCno)
# )
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



def encode(c):
	s = str(c)
	for i in range(0,(6-len(s))):
		s = "0"+s

	return s





if __name__ == "__main__" :
   f = open(argv[1],'r')
   title_list = []
   lines = f.read().splitlines()
   for item in lines:
        s = item.split(',')
        acno = ""


        #insert into the constituency list first
      #  try:
        sql = "SELECT COUNT(*) FROM Constituency"
        cur.execute(sql)
        print("Count got")
        res = cur.fetchone()
        print res
        res = res[0]
        acno = encode(res)
        print "Finding PC => "+s[len(s)-1].strip()
        sql = "SELECT PCno from Parliamentary_Constituency where PCName='"+s[len(s)-1].strip()+"'"
        cur.execute(sql)
#        x = input()

        res = cur.fetchone()
        print res
        pcno = res[0]
        sql="INSERT INTO Constituency VALUES('"+"WBAC"+acno+"','"+s[0].strip()+"',"+str(0)+",'"+pcno+"')"
        print sql
        cur.execute(sql)
        #print("Error in inserting district")
        print s

        #insert into the district table second
        #try:
        sql = "SELECT Acno FROM Constituency WHERE AcName='"+s[0].strip()+"'"
        cur.execute(sql)
        res = cur.fetchone()
        acno = res[0]
        print acno
        #print("ERROR IN GETTING THE ACno")
        print s
        sql="INSERT INTO District_Constituency VALUES('"+s[1].strip()+"','"+acno+"')"
        cur.execute(sql)
#        print("Error in inserting district")
        print s
        con.commit()


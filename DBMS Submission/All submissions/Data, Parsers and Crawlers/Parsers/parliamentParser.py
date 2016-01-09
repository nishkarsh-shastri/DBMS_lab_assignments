import MySQLdb as mdb


# def  CreateTables():
# 	con = mdb.connect('localhost', 'root', 'madeforyou', 'election')
#
# 	with con:
# 		cur = con.cursor()
# 		cur.execute("DROP TABLE IF EXISTS Constituency")
# 		cur.execute("DROP TABLE IF EXISTS Parliamentary_Constituency")
# 		cur.execute("""CREATE TABLE Parliamentary_Constituency
# 					(
# 						PCno VARCHAR(10),
# 						PCName VARCHAR(30) NOT NULL,
# 						State VARCHAR(25) NOT NULL,
# 						PRIMARY KEY(PCno)
# 					)""")
#
#
# 		cur.execute("""	CREATE TABLE Constituency (
# 						Acno Char(10),
# 						Acname VARCHAR(30) NOT NULL,
# 						Population INT,
# 						PCno VARCHAR(10),
# 						PRIMARY KEY c_pk (Acno),
# 						CONSTRAINT FOREIGN KEY c_fk(PCno) REFERENCES Parliamentary_Constituency(PCno))""")

def encode(c):
	s = str(c)
	for i in range(0,(8-len(s))):
		s = "0"+s
	return s

def insertConstituencyData():
	con = mdb.connect('localhost', 'root', 'madeforyou', 'election')

	with con:
		cur = con.cursor()
		f = open("centreData.txt","r")
		lines = f.read().splitlines()
		count = 0
		for line in lines:
			print line
			count = count + 1
			s = line.split(',')
			print s
			str1 = "INSERT INTO Parliamentary_Constituency VALUES (\'"+"PC"+encode(count)+"\', \'"+s[1]+"\'"+ ", \'"+s[0]+"\'" +")"
			print str1
			cur.execute(str1)



if __name__ == "__main__":
	# CreateTables()
	insertConstituencyData()
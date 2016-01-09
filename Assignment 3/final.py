import MySQLdb as mdb
import requests
import lxml.html

db = mdb.connect('ip_address', 'user_name', 'password', 'database_name');

def main():
 prefix = "13CS60R04"
 	
 cursor = db.cursor()
 sql = "DROP TABLE IF EXISTS "+prefix+"_M_Producer"
 #print sql
 cursor.execute(sql)
 #cursor.execute("DROP TABLE IF EXISTS %s_M_Producer",prefix)
 sql = "DROP TABLE IF EXISTS "+prefix+"_M_Director"
 cursor.execute(sql)
 


if __name__ == '__main__':
    main()

 try:
        location =(hxs.xpath('//div[@id="titleDetails"]/div[6]/a/text()'))
        lid = []
        for l in location:
            print l
            sql = "Select lid from "+prefix+"_Location WHERE location ='"+l+"'"
            cur.execute(sql)
            res = cur.fetchall();
            if len(res)==0:
                try:
                    sql = "INSERT INTO "+prefix+"_Location(location) VALUES('"+l+"')"
                    cur.execute(sql)
                    con.commit()
                except:
                    sql = ""
            sql = "Select lid from "+prefix+"_Location WHERE location ='"+l+"'"
            cur.execute(sql)
            res = cur.fetchall()
    except:
        movie['location']=""
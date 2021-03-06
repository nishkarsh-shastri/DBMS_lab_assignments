__author__ = 'nishkarsh'
import sys
import requests
import lxml.html
import MySQLdb as mdb
from time import sleep

# The global variables holding the link name and tables' prefix
link = ""
prefix = ""
con = mdb.connect('localhost', 'root', 'madeforyou', 'now')
cur = con.cursor()

def getMovie(id):
    try:
        hxs = ""
        a = 1
        while a==1:
            try:
                hxs = lxml.html.document_fromstring(requests.get("http://www.imdb.com/title/" + id).content)
                a = 0
            except:
                print "Connection error. Retrying...."
                sleep(2)
                a = 1
        hxs_castPage = ""
        a = 1
        while a==1:
            try:
                hxs_castPage = lxml.html.document_fromstring(requests.get("http://www.imdb.com/title/" + id+"/fullcredits?ref_=tt_cl_sm#cast").content)
                a = 0
            except:
                print "Connection error in cast page. Retrying...."
                sleep(2)
                a = 1
        movie = {}
        movie['mid'] = id
        try:
            movie['title'] = hxs.xpath('//*[@id="overview-top"]/h1/span[1]/text()')[0].strip()
        except IndexError:
            movie['title']
        try:
            movie['year'] = hxs.xpath('//*[@id="overview-top"]/h1/span[2]/a/text()')[0].strip()
        except IndexError:
            try:
                movie['year'] = hxs.xpath('//*[@id="overview-top"]/h1/span[3]/a/text()')[0].strip()
            except IndexError:
                movie['year'] = ""
        try:
            movie['certification'] = hxs.xpath('//*[@id="overview-top"]/div[2]/span[1]/@title')[0].strip()
        except IndexError:
            movie['certification'] = ""
        try:
            movie['running_time'] = hxs.xpath('//*[@id="overview-top"]/div[2]/time/text()')[0].strip()
        except IndexError:
            movie['running_time'] = ""
        try:
            movie['genre'] = hxs.xpath('//*[@id="overview-top"]/div[2]/a/span/text()')
            ## add this genre to the genre table if not exists
            for g in movie['genre']:
                try:
                    sql = "INSERT INTO "+prefix+"_Genre VALUES('"+g+"','"+g+"')"
                    cur.execute(sql)
                    con.commit()
                except:
                    continue
        except IndexError:
            movie['genre'] = []
        try:
            movie['release_date'] = hxs.xpath('//*[@id="overview-top"]/div[2]/span[3]/a/text()')[0].strip()
        except IndexError:
            try:
                movie['release_date'] = hxs.xpath('//*[@id="overview-top"]/div[2]/span[4]/a/text()')[0].strip()
            except Exception:
                movie['release_date'] = ""
        try:
            movie['rating'] = hxs.xpath('//*[@id="overview-top"]/div[3]/div[3]/strong/span/text()')[0]
        except IndexError:
            movie['rating'] = ""
        try:
            movie['metascore'] = hxs.xpath('//*[@id="overview-top"]/div[3]/div[3]/a[2]/text()')[0].strip().split('/')[0]
        except IndexError:
            movie['metascore'] = 0
        try:
            movie['description'] = hxs.xpath('//*[@id="overview-top"]/p[2]/text()')[0].strip()
        except IndexError:
            movie['description'] = ""
        try:
            dir_list = hxs.xpath('//*[@id="overview-top"]/div[4]/a/@href')
            movie['director'] = getPersonList(dir_list)
        except IndexError:
            movie['director'] = ""
        try:
            star_list = hxs.xpath('//div[@id="titleCast"]/table/tr/td[@itemprop="actor"]/a/@href')
            movie['stars'] = getPersonList(star_list)

        except IndexError:
            movie['stars'] = ""
        try:
            movie['poster'] = hxs.xpath('//*[@id="img_primary"]/div/a/img/@src')[0]
        except IndexError:
            movie['poster'] = ""
        try:
            movie['gallery'] = hxs.xpath('//*[@id="combined-photos"]/div/a/img/@src')
        except IndexError:
            movie['gallery'] = ""
        try:
            movie['storyline'] = hxs.xpath('//*[@id="titleStoryLine"]/div[1]/p/text()')[0].strip()
        except IndexError:
            movie['storyline'] = ""
        try:
            movie['votes'] = hxs.xpath('//*[@id="overview-top"]/div[3]/div[3]/a[1]/span/text()')[0].strip()
        except IndexError:
            movie['votes'] = ""
        try:
            prod_list = hxs_castPage.xpath('//div[@id="fullcredits_content"]/table[4]/tbody/tr/td/a/@href')
            movie['producer']=getPersonList(prod_list)
        except IndexError:
            movie['producer'] = ""
        try:
            country_id =(((hxs.xpath('//div[@id="titleDetails"]/div[2]/a/@href')[0].strip()).split('/'))[2].split('?'))[0]
            country_name = hxs.xpath('//div[@id="titleDetails"]/div[2]/a/text()')[0]
            try:
                sql = "INSERT INTO "+prefix+"_Country VALUES('"+country_id+"','"+country_name+"')"
                cur.execute(sql)
                con.commit()
            except:
                sql = ""
            movie['country'] = country_id
        except:
            movie['country']=""
        try:
            location =(hxs.xpath('//div[@id="titleDetails"]/div[6]/a/text()'))
            lid = []
            for l in location:
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
                for row in res:
                    lid.append(row[0])
            movie['location']=lid
        except:
            movie['location']= ""
        try:
            language_id =(((hxs.xpath('//div[@id="titleDetails"]/div[3]/a/@href')[0].strip()).split('/'))[2].split('?'))[0]
            language = (hxs.xpath('//div[@id="titleDetails"]/div[3]/a/text()'))

            sql = "INSERT INTO "+prefix+"_Language VALUES('"+language_id+"','"+language[0]+"')"

            try:
                cur.execute(sql)
                con.commit()
            except:
                sql = ""
            movie['language'] = language_id
        except:
            movie['language']=""

        ## Mapping in data table will start from here

        ## first one - The Movie and the Cast mapping
        mid = movie['mid']
        sql = "INSERT INTO "+prefix+"_Movie VALUES('"+mid+"','"+movie['title']+"',"+movie['year']+","+movie['rating']+","+movie['votes'].replace(",","")+")"
        try:
            cur.execute(sql)
        except:
            sql =""
        for s in movie['stars']:
            sql = "INSERT INTO "+prefix+"_M_Cast VALUES('"+mid+"','"+s+"')"
            try:
                cur.execute(sql)
                con.commit()
            except:
                continue

         ## The Movie and the Directors mapping
        for s in movie['director']:
            sql = "INSERT INTO "+prefix+"_M_Director VALUES('"+mid+"','"+s+"')"
            try:
                cur.execute(sql)
                con.commit()
            except:
                continue
        ## The Movie and the Producers mapping
        for s in movie['producer']:
            sql = "INSERT INTO "+prefix+"_M_Producer VALUES('"+mid+"','"+s+"')"
            try:
                cur.execute(sql)
                con.commit()
            except:
                continue
        for s in movie['genre']:
            sql = "INSERT INTO "+prefix+"_M_Genre VALUES('"+mid+"','"+s+"')"
            try:
                cur.execute(sql)
                con.commit()
            except:
                continue

        if movie['language']!="":
            sql = "INSERT INTO "+prefix+"_M_Language VALUES('"+mid+"','"+movie['language']+"')"
            try:
                cur.execute(sql)
                con.commit()
            except:
                sql=""


        if movie['country']!="":
            sql = "INSERT INTO "+prefix+"_M_Country VALUES('"+mid+"','"+movie['country']+"')"
            try:
                cur.execute(sql)
                con.commit()
            except:
                sql=""
        if len(movie['location'])>0:
            for s in movie['location']:

                sql = "INSERT INTO "+prefix+"_M_Location VALUES('"+mid+"','"+str(s)+"')"
                try:
                    cur.execute(sql)
                    con.commit()
                except:
                    continue

        return movie
    except:
        print "error"

def getPersonList(person):
    idlist = []

    for p in person:
        a = 1
        hxs = ""
        while a==1:
            try:
                hxs = lxml.html.document_fromstring(requests.get("http://www.imdb.com/" + p).content)
                a = 0
            except:
                sleep(2)
                a = 1
        p_id = p.split('/')[2]
        idlist.append(p_id)
        try:
            p_name = (hxs.xpath('//span[@itemprop="name"]/text()'))[0].strip()
        except:
            p_name = ""
        try:
            p_dob =  (hxs.xpath('//div[@id="name-born-info"]/time/@datetime'))[0]
        except:
            p_dob = ""
        try:
            deter =  (hxs.xpath('//div[@id="name-job-categories"]/a[1]/span/text()'))
        except:
            deter = ""
        deter = (deter[0].split('\n'))[1]

        if deter == "Actor":
            p_gender = "male"
        else:
            if deter =="Actress":
                p_gender = "female"
            else:
                p_gender = ""


        sql = "INSERT INTO "+prefix+"_Person VALUES(\'"+p_id+"\',\'"+p_name+"\',\'"+p_dob+"\',\'"+p_gender+"\')"
        try:
            cur.execute(sql)
        except:
            continue

        con.commit()
        sleep(2)
    return idlist

def createDataBase():

        sql = "CREATE TABLE IF NOT EXISTS "+prefix+"_Movie (mid VARCHAR(10),title VARCHAR(80),year INTEGER,rating DECIMAL(3,1),num_votes INTEGER, CONSTRAINT PRIMARY KEY(mid))"
        cur.execute(sql)

        sql = "CREATE TABLE IF NOT EXISTS "+prefix+"_Person (pid VARCHAR(10),name VARCHAR(80),dob DATE,gender VARCHAR(30),CONSTRAINT pk_per PRIMARY KEY(pid))"
        cur.execute(sql)

        sql = "CREATE TABLE IF NOT EXISTS "+prefix+"_Genre (gid VARCHAR(10),name VARCHAR(10),CONSTRAINT PRIMARY KEY(gid))"
        cur.execute(sql)

        sql = "CREATE TABLE IF NOT EXISTS "+prefix+"_Language (laid VARCHAR(5),name VARCHAR(20),CONSTRAINT PRIMARY KEY(laid))"
        cur.execute(sql)

        sql = "CREATE TABLE IF NOT EXISTS "+prefix+"_Country (cid VARCHAR(10),name VARCHAR(30),CONSTRAINT PRIMARY KEY(cid))"
        cur.execute(sql)

        sql = "CREATE TABLE IF NOT EXISTS "+prefix+"_Location (lid INTEGER AUTO_INCREMENT,location VARCHAR(100),CONSTRAINT pk_per PRIMARY KEY(lid))"
        cur.execute(sql)

        sql = "CREATE TABLE IF NOT EXISTS "+prefix+"_M_Producer(mid VARCHAR(10),pid VARCHAR(10),CONSTRAINT PRIMARY KEY(mid,pid), FOREIGN KEY f_mp(mid) REFERENCES "+prefix+"_Movie(mid), FOREIGN KEY f_mp2(pid) REFERENCES "+prefix+"_Person(pid))"
        cur.execute(sql)


        sql = "CREATE TABLE IF NOT EXISTS "+prefix+"_M_Director(mid VARCHAR(10),pid VARCHAR(10),CONSTRAINT PRIMARY KEY(mid,pid) ,FOREIGN KEY f_md(mid) REFERENCES "+prefix+"_Movie(mid) ,FOREIGN KEY f_md2(pid) REFERENCES "+prefix+"_Person(pid))"
        cur.execute(sql)

        sql = "CREATE TABLE IF NOT EXISTS "+prefix+"_M_Cast(mid VARCHAR(10),pid VARCHAR(10),CONSTRAINT PRIMARY KEY(mid,pid) ,FOREIGN KEY f_mc(mid) REFERENCES "+prefix+"_Movie(mid) ,FOREIGN KEY f_mc2(pid) REFERENCES "+prefix+"_Person(pid))"
        cur.execute(sql)

        sql = "CREATE TABLE IF NOT EXISTS "+prefix+"_M_Genre(mid VARCHAR(10),gid VARCHAR(10),CONSTRAINT PRIMARY KEY(mid,gid) ,FOREIGN KEY f_mg(mid) REFERENCES "+prefix+"_Movie(mid) ,FOREIGN KEY f_mg2(gid) REFERENCES "+prefix+"_Genre(gid))"
        cur.execute(sql)

        sql = "CREATE TABLE IF NOT EXISTS "+prefix+"_M_Language(mid VARCHAR(10),laid VARCHAR(5),CONSTRAINT PRIMARY KEY(mid,laid) ,FOREIGN KEY f_ml(mid) REFERENCES "+prefix+"_Movie(mid) ,FOREIGN KEY f_ml2(laid) REFERENCES "+prefix+"_Language(laid))"
        cur.execute(sql)

        sql = "CREATE TABLE IF NOT EXISTS "+prefix+"_M_Country(mid VARCHAR(10),cid VARCHAR(10),CONSTRAINT PRIMARY KEY(mid,cid) ,FOREIGN KEY f_mc(mid) REFERENCES "+prefix+"_Movie(mid) ,FOREIGN KEY f_mc2(cid) REFERENCES "+prefix+"_Country(cid))"
        cur.execute(sql)

        sql = "CREATE TABLE IF NOT EXISTS "+prefix+"_M_Location (mid VARCHAR(10),lid INTEGER,CONSTRAINT PRIMARY KEY(mid,lid) ,FOREIGN KEY f_ml1(mid) REFERENCES "+prefix+"_Movie(mid) ,FOREIGN KEY f_ml02(lid) REFERENCES "+prefix+"_Location(lid))"
        cur.execute(sql)

        con.commit()

def getTitleList(link):
    hxs = lxml.html.document_fromstring(requests.get(link).content)
    try:
        movie_list = hxs.xpath('//table[@class="results"]/tr/td[@class="title"]/span[1]/@data-tconst')
    except IndexError:
        movie_list = ""
    return movie_list

def getNextPage(link):
    hxs = lxml.html.document_fromstring(requests.get(link).content)
    try:
        nextPageAp = hxs.xpath('//div[@id="right"]/span[1]/a/@href')
        nextPage = "www.imdb.com"+nextPageAp[0]
    except:
        nextPage = ""
    return nextPage

if __name__ == "__main__":

    file = open('info.txt','r')
    link = (file.readline()).rstrip('\n')
    prefix = (file.readline()).rstrip('\n')
    file.close()
    createDataBase()
    i = 0
    while i<5:
        titleList = getTitleList(link)
        for title in titleList:
            getMovie(title)
            print title
            sleep(2)
        i = i+1
        link = getNextPage(link)
        print link

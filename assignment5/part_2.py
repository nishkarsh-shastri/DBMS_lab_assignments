__author__ = 'nishkarsh'

from sets import Set
from operator import itemgetter
import operator
import MySQLdb as mdb
import networkx as nx

con = mdb.connect('10.5.18.66', '12CS10034', 'btech12', '12CS10034')
cur = con.cursor()

def findAnswer():
    # Initial SQL queries
    sql = "create or replace view vcast as select mid,pid from 12CS10034_Movie Natural Join 12CS10034_M_Cast"
    cur.execute(sql)

    sql = "select distinct A.pid,B.pid from vcast A,vcast B where A.mid = B.mid and A.pid>B.pid"
    cur.execute(sql)

    # Construct the graph using the edges obtained above
    g = nx.Graph()
    for x in cur.fetchall():
        i = -1
        v1 = ""
        v2 = ""
        for y in x:
            i=i+1
            if(i==0):
                v1=y
            elif(i==1):
                v2=y
                i=-1
        g.add_edge(v1,v2)
        g.add_edge(v2,v1)

    #Just for output purpose, print the number of edges
    print g.number_of_edges()
    path = nx.all_pairs_shortest_path_length(g) # Call the function to get all pair shortest path length
    i = 0

    # get the list of all the pid,name pair. We will use this mapping to create the name combination
    sql = "select pid,name from 12CS10034_Person"
    cur.execute(sql)
    name_dict = {}
    for x in cur.fetchall():
        name_dict[x[0]]=x[1]

    compl = [] # the list that will contain pid of all the casts
    sql = "select distinct pid from 12CS10034_M_Cast natural join 12CS10034_Person"
    cur.execute(sql)
    for x in cur.fetchall():
        compl.append(x[0]) #append the pairs in a fullset, so that we can find those pair who are having no involvement in the graph
    print len(compl)


    print len(name_dict) #just for output purpose
    fullSet = Set(compl) # get the full set of actors



    tuplelist = [] #tuples to add to the table
    vertexlist = Set() #this will help us to get the remaining non participating nodes

    for x in path:
            vertexlist.add(x)
            halflist = Set() #vertices not present in this list
            for k in path[x]:
                t = (x,name_dict[x],k,name_dict[k],path[x][k])
                tuplelist.append(t)
                halflist.add(k)
            diff = fullSet-halflist
            for k in diff:
                t = (x,name_dict[x],k,name_dict[k],-1) #no edge exist for these ones
                tuplelist.append(t)

    diff = fullSet - vertexlist
    for x in diff: # no edge exist for these ones
        for k in fullSet:
            if(x!=k):
                t = (x,name_dict[x],k,name_dict[k],-1)
                tuplelist.append(t)

    #sort the tuple list, unfortunately the insertion is not happening in sorted order
    tuplelist = sorted(tuplelist,key = itemgetter(1,3))
    print len(tuplelist)
    m = 0
    for i in tuplelist: # to see the sorted ordering
        if(m<100):
            print i
            m = m+1
        else:
            break
    for i in tuplelist:
        if(i[4]!=0):
            sql = "INSERT INTO 12CS10034_separate VALUES('"+i[0]+"','"+i[1]+"','"+i[2]+"','"+i[3]+"',"+str(i[4])+")" # insert into the table all the pid and name
            cur.execute(sql)
    con.commit()

    sql = "INSERT INTO 12CS10034_orderedSeparation(actor_1,actor_2,separation) select actor_1,actor_2,separation from 12CS10034_separate order by actor_1,actor_2 asc" # get ordered table as desired in the question
    cur.execute(sql)
    con.commit()

    # sql = "DROP TABLE 12CS10034_separate" # drop the earlier created table.
    # cur.execute(sql)
    # con.commit()


if __name__ == "__main__":

    sql = "CREATE TABLE IF NOT EXISTS 12CS10034_separate(pid1 VARCHAR(9),actor_1 VARCHAR(50),pid2 VARCHAR(9),actor_2 VARCHAR(50),separation integer,constraint primary key(pid1,pid2))"
    cur.execute(sql)
    sql = "CREATE TABLE IF NOT EXISTS 12CS10034_orderedSeparation(actor_1 VARCHAR(50),actor_2 VARCHAR(50),separation integer)" # note that there will be no primary key in this table as names can be repeated
    cur.execute(sql)
    findAnswer()


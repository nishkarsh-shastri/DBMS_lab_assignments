Find the pair of similar movies

1)

#  To create the edge graph, use the following query which would give output all the edge(v1,v2)
select distinct T.mid,P.mid 
from 12CS10034_Movie  Natural join 12CS10034_M_Cast as T,
12CS10034_Movie as P 
where T.pid in 
(select pid from 12CS10034_Movie natural join 12CS10034_M_Cast where mid =P.mid and mid !=T.mid)
and T.mid > P.mid

#alternate

create or replace view vcast as select mid,pid from 12CS10034_Movie Natural Join 12CS10034_M_Cast;

select distinct A.mid,B.mid from vcast A,vcast B where A.pid = B.pid and A.mid > B.mid


# Run the python script named part_1.py to know the size of maximum clique



2a) Find the edge graph of actors


# Use the script. 
#  To create the edge graph, use the following query which would give output all the edge(v1,v2)
create or replace view vcast as select mid,pid from 12CS10034_Movie Natural Join 12CS10034_M_Cast;

select distinct A.pid,B.pid from vcast A,vcast B where A.mid = B.mid and A.pid>B.pid;	

# Now run the python script part_2.py to create 12CS10034_orderedSeparation table for all pair of actors

Main QUERY: 
select * from 12CS10034_orderedSeparation

2b) 
# First run the part_2b.py script to create the table 12CS10034_canfind.
# Then for any pair of value you can get answer column which tells whether actor 2 can be found by knowledge of actor_1
select * from 12CS10034_canfind

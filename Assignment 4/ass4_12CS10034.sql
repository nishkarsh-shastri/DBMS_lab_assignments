QUERY SET 1



a) 
SELECT pratip_Person.PID, pratip_Person.name,pratip_Movie.title ,pratip_Movie.year
FROM pratip_Movie 
NATURAL JOIN pratip_M_Director 
NATURAL JOIN pratip_Person 
WHERE year%4=0 
AND 
mid IN (
	SELECT mid 
	FROM pratip_Movie 
	NATURAL JOIN pratip_M_Genre 
	NATURAL JOIN pratip_Genre 
	WHERE pratip_Genre.name = 'Comedy'
	);
b)

SELECT pid,name,dob 
FROM pratip_Movie 
NATURAL JOIN pratip_M_Cast 
NATURAL JOIN pratip_Person 
WHERE pratip_Movie.title='Anand';


c)
SELECT DISTINCT pid,name
FROM pratip_Movie
NATURAL JOIN pratip_M_Cast
NATURAL JOIN pratip_Person
WHERE pratip_Movie.year < 1970
AND pid IN
(
	SELECT DISTINCT pid 
	FROM pratip_Movie 
	NATURAL JOIN pratip_M_Cast 
	NATURAL JOIN pratip_Person 
	WHERE pratip_Movie.year > 1990
);

d)
SELECT pid,name,dob,COUNT(*) AS numberOfMovies
FROM pratip_Movie
NATURAL JOIN pratip_M_Director
NATURAL JOIN pratip_Person
GROUP BY pid
HAVING numberOfMovies>=10
ORDER BY numberOfMovies DESC;


e)

(i)
SELECT distinct mid,title,year,count(distinct mid) FROM pratip_Movie NATURAL JOIN pratip_M_Cast NATURAL JOIN pratip_Person
where Gender = 'Female' and mid not in (SELECT mid FROM pratip_Movie NATURAL JOIN pratip_M_Cast NATURAL JOIN pratip_Person WHERE Gender='Male' or Gender='NULL')
GROUP BY year;

(ii)


CREATE OR REPLACE VIEW VC as 
SELECT distinct mid,title,year,count(distinct mid) as C FROM pratip_Movie NATURAL JOIN pratip_M_Cast NATURAL JOIN pratip_Person
where Gender = 'Female' and mid not in (SELECT mid FROM pratip_Movie NATURAL JOIN pratip_M_Cast NATURAL JOIN pratip_Person WHERE Gender='Male' or Gender='NULL')
GROUP BY year;

CREATE OR REPLACE VIEW VD AS 
SELECT year as m_year,count(*) as count_movies from pratip_Movie GROUP by year;
SELECT A.C , count_movies, (A.C/count_movies)*100 FROM VD D,VC A WHERE A.year = D.m_year; 	

DROP VIEW VC,VD;



f)

CREATE VIEW mcast AS SELECT COUNT(*) AS castCount FROM pratip_M_Cast GROUP BY MID;

SELECT DISTINCT mid,title,count(*) as sizeOfCast
FROM pratip_Movie NATURAL JOIN pratip_M_Cast
GROUP BY mid
HAVING sizeOfCast = (select Max(castCount) FROM mcast GROUP BY mid);

DROP VIEW mcast;

g)
	
CREATE OR REPLACE view V
AS 
SELECT year,count(MID) as count
FROM pratip_Movie 
GROUP BY year;

CREATE OR REPLACE VIEW W 
as 
SELECT year as start,year + 9 as end,
(SELECT SUM(count) FROM V Z where Z.year>=X.year and Z.year<X.year+10) as count 
FROM V X;

SELECT start,end,count 
FROM W
WHERE count = (SELECT MAX(count) from W);



h)
/*CREATE OR REPLACE VIEW V AS
SELECT pid,mid,name,year
FROM pratip_Movie NATURAL JOIN pratip_M_Cast
NATURAL JOIN pratip_Person;

SELECT DISTINCT A.name 
FROM V A 
INNER JOIN 
V B 
ON (A.pid = B.pid) 
WHERE 
(A.year + 3 <=B.year OR A.year-3>=B.year) 
AND A.mid !=B.mid;
*/
CREATE OR REPLACE VIEW v_h AS
SELECT *
FROM pratip_M_Cast
NATURAL JOIN pratip_Person
NATURAL JOIN pratip_Movie;

SELECT DISTINCT t.name,t.pid
FROM v_h AS t
WHERE pid NOT IN
(SELECT DISTINCT t1.pid
FROM v_h AS t1
LEFT JOIN v_h AS t2 ON t1.pid = t2.pid
AND t1.YEAR > t2.YEAR
AND t1.YEAR <= t2.YEAR + 3
WHERE t1.YEAR !=
(SELECT YEAR
FROM v_h AS t3
WHERE t3.pid = t1.pid
GROUP BY YEAR
ORDER BY YEAR LIMIT 1)
AND t2.YEAR IS NULL)
ORDER BY t.name;


i) 

SELECT distinct pid,name FROM pratip_M_Cast NATURAL JOIN pratip_Person WHERE pid in(
SELECT P from (
SELECT distinct pratip_M_Cast.pid as P,count(*) as C
FROM pratip_Movie
NATURAL JOIN pratip_M_Cast
INNER JOIN pratip_M_Director
On pratip_M_Cast.MID = pratip_M_Director.MID
INNER JOIN pratip_Person
On pratip_M_Director.pid = pratip_Person.pid
WHERE pratip_Person.name = 'Yash chopra'
GROUP BY pratip_M_Cast.pid
HAVING C > ALL
(
SELECT count(*)
FROM pratip_Movie
NATURAL JOIN pratip_M_Cast
RIGHT OUTER JOIN pratip_M_Director
On pratip_M_Cast.MID = pratip_M_Director.MID
INNER JOIN pratip_Person
On pratip_M_Director.pid = pratip_Person.pid
WHERE pratip_Person.name != 'Yash chopra'
AND pratip_M_Cast.pid = P
GROUP BY pratip_M_Cast.pid,pratip_M_Director.pid
)
)y
);

j)

CREATE OR REPLACE VIEW V AS
SELECT pid,name,mid FROM pratip_Movie 
NATURAL JOIN pratip_M_Cast
NATURAL JOIN pratip_Person;



CREATE OR REPLACE VIEW SRK1 AS
SELECT DISTINCT B.pid as pid,B.name as name
FROM V B 
WHERE B.MID IN
(
SELECT DISTINCT MID 
FROM V A 
WHERE Name = 'Shah Rukh Khan'
) 
AND B.Name != 'Shah Rukh Khan';


SELECT DISTINCT D.pid, D.name FROM V D WHERE D.MID IN
(
SELECT DISTINCT C.MID 
FROM V C 
WHERE C.pid IN
(
	SELECT pid FROM SRK1
) 
AND C.MID NOT IN (SELECT DISTINCT MID FROM V WHERE Name = 'Shah Rukh Khan')
)
AND D.pid NOT IN 
(
SELECT pid FROM SRK1
);





--------------Query Set 2------------------------------------------------

a)
SELECT Title, count(*) as Cast_List_Size
from pratip_Movie
NATURAL JOIN
pratip_M_Cast
WHERE pratip_Movie.year = 1970
GROUP BY pratip_Movie.mid
ORDER BY Cast_List_Size DESC;

b)
SELECT pratip_Person.name, pratip_M_Cast.pid,count(*) as movies_after_1990
FROM pratip_Movie
NATURAL JOIN pratip_M_Cast
NATURAL JOIN pratip_Person
WHERE pratip_Movie.year>1990
GROUP BY pratip_M_Cast.pid
HAVING movies_after_1990>=13;


c)
CREATE VIEW CN AS
SELECT * FROM pratip_M_Cast NATURAL JOIN pratip_Person;

SELECT *, COUNT(*) as C
FROM CN A
INNER JOIN CN B
on A.mid = B.mid
GROUP BY A.name,B.name
HAVING C > 10;

DROP VIEW CN;


d)

CREATE OR REPLACE VIEW MCN AS
SELECT * FROM pratip_Movie NATURAL JOIN pratip_M_Cast NATURAL JOIN pratip_Person GROUP BY pratip_Movie.MID;

SELECT A.pid,A.name,A.title,B.title
FROM  MCN A
INNER JOIN MCN B
ON A.pid = B.pid
WHERE (A.title LIKE 'A%' OR A.Title LIKE 'S%')
AND (B.title LIKE 'A%' OR B.title LIKE 'S%')
AND A.title != B.title;





e)
SELECT pratip_Movie.year, Count(*) as numberOfMovies,pratip_Person.name,pratip_Person.pid
FROM pratip_Movie
NATURAL JOIN pratip_M_Cast
NATURAL JOIN pratip_Person
WHERE pratip_Person.name = 'Amitabh Bachchan'
GROUP BY pratip_Movie.year
HAVING 
numberOfMovies >= 
ALL(
	SELECT COUNT(*) as C
	FROM pratip_Movie
	NATURAL JOIN pratip_M_Cast
	NATURAL JOIN pratip_Person
	WHERE pratip_Person.name = 'Amitabh Bachchan'
GROUP BY pratip_Movie.year
);

f)

SELECT DISTINCT t2.pid,t2.name,t2.mid 
FROM
(
SELECT pratip_Person.pid,pratip_Person.name,pratip_M_Cast.mid
FROM pratip_M_Cast
NATURAL JOIN pratip_Person
WHERE pratip_Person.name = 'Om Puri'
) t1
INNER JOIN
(
SELECT pratip_Person.pid,pratip_Person.name,pratip_M_Cast.mid
FROM pratip_M_Cast
NATURAL JOIN pratip_Person
WHERE pratip_Person.name != 'Om Puri'
) t2
ON t1.mid = t2.mid


g)	

(a)

CREATE OR REPLACE VIEW CN AS
SELECT * FROM pratip_M_Cast NATURAL JOIN pratip_Person;

CREATE OR REPLACE VIEW DN AS
SELECT * FROM pratip_M_Director NATURAL JOIN pratip_Person;

SELECT A.pid as N,A.name,B.pid as D,B.name, COUNT(*) as E
FROM CN A
INNER JOIN DN B
on A.mid = B.mid
GROUP BY N,D
HAVING E = 
(
SELECT MAX(C)
FROM 
(
SELECT count(*) as C
FROM CN X
INNER JOIN DN Y
on X.mid = Y.mid
GROUP BY X.name, Y.name
) 
y);

(b)

CREATE OR REPLACE VIEW PN AS
SELECT * FROM pratip_M_Producer NATURAL JOIN pratip_Person;


SELECT A.pid as N,A.name,B.pid as D,B.name, COUNT(*) as E
FROM CN A
INNER JOIN PN B
on A.mid = B.mid
GROUP BY N,D
HAVING E = 
(
SELECT MAX(C)
FROM 
(
SELECT count(*) as C
FROM CN X
INNER JOIN PN Y
on X.mid = Y.mid
GROUP BY X.name, Y.name
) 
y);



h)

	SELECT t1.name, t1.pid,t2.mid,count(*) as C
FROM
(
SELECT pratip_Person.name, pratip_Person.pid,pratip_Movie.mid as m
FROM pratip_Movie
NATURAL JOIN pratip_M_Cast
NATURAL JOIN pratip_Person
) t1
INNER JOIN
(
SELECT mid 
FROM pratip_Movie
WHERE title LIKE 'Dhoom%'
) t2
ON t1.m = t2.mid
GROUP BY t1.pid
HAVING C = 
(
SELECT count(*)
FROM pratip_Movie
WHERE title LIKE 'Dhoom%'
) ;


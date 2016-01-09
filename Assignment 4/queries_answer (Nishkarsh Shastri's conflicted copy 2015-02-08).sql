1) 
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
	WHERE pratip_Genre.name = 'Action'
	);
2) 
SELECT pid,name,dob 
FROM pratip_Movie 
NATURAL JOIN pratip_M_Cast 
NATURAL JOIN pratip_Person 
WHERE pratip_Movie.title='Anand';
3)
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
	WHERE pratip_Movie.year > 1970
);
4)
SELECT pid,name,dob,COUNT(*) AS numberOfMovies
FROM pratip_Movie
NATURAL JOIN pratip_M_Director
NATURAL JOIN pratip_Person
GROUP BY pid
HAVING numberOfMovies>10
ORDER BY numberOfMovies DESC;
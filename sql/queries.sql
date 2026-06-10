-- Question 1
insert into cd.facilities values (9, 'Spa', 20, 30, 100000, 800);

-- Question 2
insert into cd.facilities values 
	((SELECT facid FROM cd.facilities ORDER BY facid DESC LIMIT 1)+1,'Spa', 20, 30, 100000, 800);


-- Question 3
UPDATE cd.facilities
SET initialoutlay=10000
WHERE facid=1;

-- Question 4
update cd.facilities
SET membercost=(SELECT membercost FROM cd.facilities WHERE facid=0)*1.1,
	guestcost=(SELECT guestcost FROM cd.facilities WHERE facid=0)*1.1
WHERE facid=1

-- Question 5
DELETE 
FROM cd.bookings;

-- Question 6
DELETE
FROM cd.members
WHERE memid=37;

-- Question 7
SELECT facid, name, membercost, monthlymaintenance
FROM cd.facilities
WHERE membercost< (monthlymaintenance/50) and membercost>0;

-- Question 8
SELECT * FROM cd.facilities
WHERE name LIKE '%Tennis%';

-- Question 9
(SELECT * FROM cd.facilities
Where facid =1)

union
(SELECT * FROM cd.facilities
Where facid =5)

-- Question 10
SELECT memid, surname, firstname, joindate
FROM cd.members
WHERE joindate>'2012-09-01';

-- Question 11
(SELECT surname
FROM cd.members)

UNION

(SELECT name
From cd.facilities);

-- Question 12
SELECT b.starttime
FROM cd.bookings b 
INNER JOIN cd.members m USING (memid)
WHERE m.firstname ='David' AND m.surname='Farrell';

-- Question 13
SELECT b.starttime as "start", f.name
FROM cd.bookings b
INNER JOIN cd.facilities f USING (facid)
WHERE f.name LIKE 'Tennis Court %'
		AND b.starttime >='2012-09-21' AND b.starttime < '2012-09-22'
	ORDER BY b.starttime;

-- Question 14
SELECT m.firstname as "memfname", m.surname as "memsname", r.firstname as "recfname", r.surname as "recsname"
FROM cd.members m
LEFT JOIN cd.members r ON m.recommendedby =r.memid
ORDER BY m.surname, m.firstname;

-- Question 15
SELECT DISTINCT r.firstname, r.surname
FROM cd.members m
INNER JOIN cd.members r ON m.recommendedby = r.memid
ORDER BY r.surname, r.firstname;

-- Question 16
SELECT DISTINCT (mem.firstname || ' ' || mem.surname) as "member",
(
  	SELECT (rec.firstname || ' ' || rec.surname) as "recommender"
 	FROM cd.members rec
 	where rec.memid= mem.recommendedby
  )
FROM cd.members mem
ORDER BY member;

-- Question 17
SELECT DISTINCT recommendedby, COUNT(memid) AS "count"
FROM cd.members
WHERE recommendedby is not null
GROUP BY recommendedby
ORDER BY recommendedby;

-- Question 18
SELECT facid, SUM(slots) AS "Total Slots"
FROM cd.bookings
Group by facid
ORDER BY facid;

-- Question 19
SELECT facid, SUM(slots) AS "Total Slots"
FROM cd.bookings
where starttime>='2012-09-01' and starttime<'2012-10-01'
Group by facid
ORDER BY "Total Slots";

-- Question 20
SELECT facid, EXTRACT(Month FROM starttime) AS "month",SUM(slots) AS "Total Slots"
FROM cd.bookings
where starttime>='2012-01-01' and starttime<'2013-01-01'
Group by facid, "month"
ORDER BY facid, "month";

-- Question 21
SELECT COUNT(DISTINCT memid) as "count"
FROM cd.members m INNER JOIN cd.bookings USING (memid);

-- Question 22
WITH  filtered AS (
  	SELECT m.surname, m.firstname, m.memid, b.starttime,
  		ROW_NUMBER() OVER (PARTITION BY m.memid ORDER BY starttime) as "rn"
	FROM cd.members m Inner join cd.bookings b USING (memid)
	WHERE b.starttime >'2012-09-01'
	ORDER BY m.memid
)

SELECT surname,firstname, memid, starttime
FROM filtered
WHERE rn=1;

-- Question 23
SELECT (SELECT COUNT(*) FROM cd.members) AS "COUNT", firstname, surname
FROM cd.members
ORDER BY joindate;

-- Question 24
SELECT ROW_NUMBER() OVER (ORDER BY m.memid), m.firstname, m.surname
FROM cd.members m
ORDER BY m.joindate;

-- Question 25
SELECT facid, total FROM
(
  	SELECT DISTINCT facid, SUM(slots) as total, RANK() OVER(ORDER BY SUM(slots) DESC) AS rank
	 FROM cd.bookings
	 GROUP BY facid
)
WHERE rank=1

-- Question 26
SELECT (surname || ', ' ||firstname) AS "name"
FROM cd.members;

-- Question 27
SELECT memid, telephone
FROM cd.members
WHERE telephone LIKE '(___)%';

-- Question 28
  SELECT substr(surname,1,1) AS letter, COUNT(substr(surname,1,1)) AS "count"
  FROM cd.members
  GROUP BY substr(surname,1,1)
  ORDER BY letter;






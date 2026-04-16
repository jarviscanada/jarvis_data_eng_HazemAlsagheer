# Introduction
This RDBMS and SQL project focuses on building practical experience with relational databases and using SQL to solve data-driven problems. It emphasizes data modeling to design structured, consistent, and reliable database schemas. The project includes 28 SQL problems covering a range of query patterns and scenarios, helping develop a solid understanding of real-world database operations and analysis.


# SQL Queries

## Table Setup
### Members table
```
CREATE TABLE IF NOT EXISTS members (
	memid 			INTEGER NOT NULL,
	surname 		VARCHAR(200) NOT NULL,
	firstname 		VARCHAR(200) NOT NULL,
	address 		VARCHAR(300) NOT NULL,
	zipcode			INTEGER NOT NULL,
	telephone		VARCHAR(20) NOT NULL,
	recommendedby	INTEGER,
	joindate		timestamp NOT NULL,
	CONSTRAINT pk_members PRIMARY KEY (memid),
	CONSTRAINT fk_members FOREIGN KEY (recommendedby) REFERENCES members(memid) ON DELETE SET NULL 
	
);
```
### Bookings Table
```
CREATE TABLE IF NOT EXISTS bookings (  
	bookid		INTEGER NOT NULL,  
	faceid		INTEGER NOT NULL,  
	memid		INTEGER NOT NULL,    
	starttime	timestamp NOT NULL,  
	slots		INTEGER NOT NULL,  
	CONSTRAINT pk_bookings PRIMARY KEY (bookid),  
	CONSTRAINT fk_faceid_bookings FOREIGN KEY (faceid) REFERENCES cd.facilities(faceid),  
	CONSTRAINT fk_memid_bookings FOREIGN KEY (memid) REFERENCES cd.members(memid)  
);
```
### Facilities Table
```
CREATE TABLE IF NOT EXISTS cd.facilities (
	faceid				INTEGER NOT NULL,
	name				VARCHAR(100) NOT NULL,
	membercost			NUMERIC NOT NULL,
	guestcost			NUMERIC NOT NULL,
	initialoutlay		NUMERIC NOT NULL,
	monthlymaintenance 	NUMERIC NOT NULL,
	CONSTRAINT pk_facilities PRIMARY KEY (faceid)
);
```

## Logical ERD

![ERD](ERD.png)
This logical ERD illustrates the database structure by defining its entities and their relationships. The cd.members entity has a recursive one-to-many relationship through the recommendedby foreign key, where a member can recommend zero or many other members, and each member can be recommended by zero or one member. The cd.bookings entity acts as a join table between cd.members and cd.facilities, capturing bookings made by members for facilities. As a result, a member can have zero or many bookings, and a facility can have zero or many bookings, while each booking is associated with exactly one member and one facility.

## SQL Questions & Solutions

### Question 1 
The club is adding a new facility - a spa. We need to add it into the facilities table. Use the following values:  
facid: 9, Name: 'Spa', membercost: 20, guestcost: 30, initialoutlay: 100000, monthlymaintenance: 800.

### Solution:
```
insert into cd.facilities values (9, 'Spa', 20, 30, 100000, 800);
```

### Question 2
Let's try adding the spa to the facilities table again. This time, though, we want to automatically generate the value for the next facid, rather than specifying it as a constant. Use the following values for everything else:  
Name: 'Spa', membercost: 20, guestcost: 30, initialoutlay: 100000, monthlymaintenance: 800.

### Solution:
```
insert into cd.facilities values ((SELECT facid FROM cd.facilities ORDER BY facid DESC LIMIT 1)+1,'Spa', 20, 30, 100000, 800);
```

### Question 3
We made a mistake when entering the data for the second tennis court. The initial outlay was 10000 rather than 8000: you need to alter the data to fix the error.

### Solution:
```
UPDATE cd.facilities
SET initialoutlay=10000
WHERE facid=1;
```

### Question 4
We want to alter the price of the second tennis court so that it costs 10% more than the first one. Try to do this without using constant values for the prices, so that we can reuse the statement if we want to.

### Solution:
```
update cd.facilities
SET membercost=(SELECT membercost FROM cd.facilities WHERE facid=0)*1.1,
	guestcost=(SELECT guestcost FROM cd.facilities WHERE facid=0)*1.1
WHERE facid=1
```

### Question 5
As part of a clearout of our database, we want to delete all bookings from the cd.bookings table. How can we accomplish this?

### Solution:
```
DELETE 
FROM cd.bookings;
```

### Question 6
We want to remove member 37, who has never made a booking, from our database. How can we achieve that?

### Solution:
```
DELETE 
FROM cd.members
WHERE memid=37;
```

### Question 7
How can you produce a list of facilities that charge a fee to members, and that fee is less than 1/50th of the monthly maintenance cost? Return the facid, facility name, member cost, and monthly maintenance of the facilities in question.

### Solution:
```
SELECT facid, name, membercost, monthlymaintenance
FROM cd.facilities
WHERE membercost< (monthlymaintenance/50) and membercost>0;
```
### Question 8
How can you produce a list of all facilities with the word 'Tennis' in their name?

### Solution:
```
SELECT * FROM cd.facilities
WHERE name LIKE '%Tennis%';
```

### Question 9
How can you retrieve the details of facilities with ID 1 and 5? Try to do it without using the OR operator.

### Solution:
```
(SELECT * FROM cd.facilities
Where facid =1)

union 
(SELECT * FROM cd.facilities
Where facid =5)
```

### Question 10
How can you produce a list of members who joined after the start of September 2012? Return the memid, surname, firstname, and joindate of the members in question.

### Solution:
```
SELECT memid, surname, firstname, joindate
FROM cd.members
WHERE joindate>'2012-09-01';
```

### Question 11
You, for some reason, want a combined list of all surnames and all facility names. Yes, this is a contrived example :-). Produce that list!

### Solution:
```
(SELECT surname
FROM cd.members)

UNION

(SELECT name
From cd.facilities);
```

### Question 12
How can you produce a list of the start times for bookings by members named 'David Farrell'?

### Solution:
```
SELECT b.starttime
FROM cd.bookings b 
INNER JOIN cd.members m USING (memid)
WHERE m.firstname ='David' AND m.surname='Farrell';
```

### Question 13
How can you produce a list of the start times for bookings for tennis courts, for the date '2012-09-21'? Return a list of start time and facility name pairings, ordered by the time.

### Solution:
```
SELECT b.starttime as "start", f.name
FROM cd.bookings b 
INNER JOIN cd.facilities f USING (facid)
WHERE f.name LIKE 'Tennis Court %' 
		AND b.starttime >='2012-09-21' AND b.starttime < '2012-09-22'
	ORDER BY b.starttime;
```

### Question 14
How can you output a list of all members, including the individual who recommended them (if any)? Ensure that results are ordered by (surname, firstname).

### Solution:
```
SELECT m.firstname as "memfname", m.surname as "memsname", r.firstname as "recfname", r.surname as "recsname"
FROM cd.members m
LEFT JOIN cd.members r ON m.recommendedby =r.memid
ORDER BY m.surname, m.firstname;
```

### Question 15
How can you output a list of all members who have recommended another member? Ensure that there are no duplicates in the list, and that results are ordered by (surname, firstname).

### Solution:
```
SELECT DISTINCT r.firstname, r.surname
FROM cd.members m
INNER JOIN cd.members r ON m.recommendedby = r.memid
ORDER BY r.surname, r.firstname;
```

### Question 16
How can you output a list of all members, including the individual who recommended them (if any), without using any joins? Ensure that there are no duplicates in the list, and that each firstname + surname pairing is formatted as a column and ordered.

### Solution:
```
SELECT DISTINCT (mem.firstname || ' ' || mem.surname) as "member",
(
  	SELECT (rec.firstname || ' ' || rec.surname) as "recommender"
 	FROM cd.members rec
 	where rec.memid= mem.recommendedby
  )
FROM cd.members mem
ORDER BY member;
```

### Question 17
Produce a count of the number of recommendations each member has made. Order by member ID.
### Solution:
```
SELECT DISTINCT recommendedby, COUNT(memid) AS "count"
FROM cd.members
WHERE recommendedby is not null
GROUP BY recommendedby
ORDER BY recommendedby;
```

### Question 18
Produce a list of the total number of slots booked per facility. For now, just produce an output table consisting of facility id and slots, sorted by facility id.

### Solution: 
```
SELECT facid, SUM(slots) AS "Total Slots"
FROM cd.bookings
Group by facid
ORDER BY facid;
```

### Question 19
Produce a list of the total number of slots booked per facility in the month of September 2012. Produce an output table consisting of facility id and slots, sorted by the number of slots.

### Solution:
```
SELECT facid, SUM(slots) AS "Total Slots"
FROM cd.bookings
where starttime>='2012-09-01' and starttime<'2012-10-01'
Group by facid
ORDER BY "Total Slots";
```

### Question 20
Produce a list of the total number of slots booked per facility per month in the year of 2012. Produce an output table consisting of facility id and slots, sorted by the id and month.

### Solution:
```
SELECT facid, EXTRACT(Month FROM starttime) AS "month",SUM(slots) AS "Total Slots"
FROM cd.bookings
where starttime>='2012-01-01' and starttime<'2013-01-01'
Group by facid, "month"
ORDER BY facid, "month";
```

### Question 21
Find the total number of members (including guests) who have made at least one booking.

### Solution:
```
SELECT COUNT(DISTINCT memid) as "count"
FROM cd.members m INNER JOIN cd.bookings USING (memid);
```

### Question 22
Produce a list of each member name, id, and their first booking after September 1st 2012. Order by member ID.

### Solution:
```
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

```

### Question 23
Produce a list of member names, with each row containing the total member count. Order by join date, and include guest members.

### Solution:
```
SELECT (SELECT COUNT(*) FROM cd.members) AS "COUNT", firstname, surname
FROM cd.members
ORDER BY joindate;
```

### Question 24
Produce a monotonically increasing numbered list of members (including guests), ordered by their date of joining. Remember that member IDs are not guaranteed to be sequential.

### Solution:
```
SELECT ROW_NUMBER() OVER (ORDER BY m.memid), m.firstname, m.surname
FROM cd.members m
ORDER BY m.joindate;
```

### Question 25
Output the facility id that has the highest number of slots booked. Ensure that in the event of a tie, all tieing results get output.

### Solution:
```
SELECT facid, total FROM 
(
  	SELECT DISTINCT facid, SUM(slots) as total, RANK() OVER(ORDER BY SUM(slots) DESC) AS rank
	 FROM cd.bookings
	 GROUP BY facid
)
WHERE rank=1
```

### Question 26
Output the names of all members, formatted as 'Surname, Firstname'

### Solution:
```
SELECT (surname || ', ' ||firstname) AS "name" 
FROM cd.members;
```

### Question 27
You've noticed that the club's member table has telephone numbers with very inconsistent formatting. You'd like to find all the telephone numbers that contain parentheses, returning the member ID and telephone number sorted by member ID.

### Solution:
```
SELECT memid, telephone
FROM cd.members
WHERE telephone LIKE '(___)%';
```

### Question 28
You'd like to produce a count of how many members you have whose surname starts with each letter of the alphabet. Sort by the letter, and don't worry about printing out a letter if the count is 0.

### Solution:
```
  SELECT substr(surname,1,1) AS letter, COUNT(substr(surname,1,1)) AS "count"
  FROM cd.members
  GROUP BY substr(surname,1,1)
  ORDER BY letter;
  
```

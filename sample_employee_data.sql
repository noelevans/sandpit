CREATE TABLE Employee 
    (EmpID INT NOT NULL , 
     EmpName VARCHAR(50) NOT NULL PRIMARY KEY, 
     JobTitle VARCHAR(50) NULL, 
     Department VARCHAR(50) NULL);
    
INSERT INTO Employee 
	(EmpID, EmpName, JobTitle, Department)
VALUES 
	(1, 'CHIN YEN', 'LAB ASSISTANT', 'LAB'),
	(2, 'MIKE PEARL', 'SENIOR ACCOUNTANT', 'ACCOUNTS'),
	(3, 'GREEN FIELD', 'ACCOUNTANT', 'ACCOUNTS'),
	(4, 'DEWANE PAUL', 'PROGRAMMER', 'IT'),
	(5, 'MATTS', 'SR. PROGRAMMER', 'IT'),
	(6, 'PLANK OTO', 'ACCOUNTANT', 'ACCOUNTS');

CREATE TABLE Address 
    (Department VARCHAR(50) NOT NULL,
     OfficeName VARCHAR(50) NOT NULL,
     Floor INT NOT NULL);
    
INSERT INTO Address 
	(Department, OfficeName, Floor)
VALUES 
	('LAB', 'CHISWELL ST', 1),
	('ACCOUNTS', 'LONDON WALL', 1),
	('IT', 'CHISWELL ST', 2);


-- Where does the oldest (earliest EmpID) member of staff work?
select * 
from Employee e 
join (select min(EmpID) from Employee) f
on e.EmpID = f.EmpID;
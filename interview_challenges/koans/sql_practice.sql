create table Employee   (id integer not null, name text, age integer, dept_id integer);
create table Department (id integer not null, dept_name text);

insert into Employee values (11, "Anna",  37, 3);
insert into Employee values (12, "Barry", 21, 3);
insert into Employee values (13, "Clare", 50, 4);
insert into Employee values (14, "Danny", 42, 4);
insert into Employee values (15, "Eric",  52, 4);

insert into Department values (3, "Advertising");
insert into Department values (4, "Finance");

-- oldest worker
select name, max(age) from Employee;
-- Eric|52

-- oldest worker by department
select name, max(age) from Employee group by dept_id;
-- Anna|37
-- Eric|52

-- duplicate entry
--insert into Department values (4, "Finance");

-- find duplicates
select   count(dept_name), dept_name 
from     Department 
group by dept_name 
having   count(dept_name) > 1;

-- orphaned employee
insert into Employee values (88, "Fred", 33, 9);

-- find orphaned employees
select * from Employee e
left join Department d on e.dept_id = d.id
where d.dept_name is null;

-- alternative way to get orphaned employees
select * from Employee where dept_id not in (select id from Department);

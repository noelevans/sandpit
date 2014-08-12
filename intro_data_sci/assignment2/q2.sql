-- select * from A;
-- select ' ';
-- select * from B;

select value, row_num, col_num from A where row_num = 2;
select ' ';
select value, row_num, col_num from B where col_num = 3;

-- Multiply the values from row 2 of A with the 
-- corresponding COLUMNS of B and sum total of multiplications

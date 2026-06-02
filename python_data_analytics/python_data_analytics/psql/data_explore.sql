--Show Table schema; Run the command below in psql CLI for schema desription.
\d+ retail;

-- Q1 Show first 10 rows
SELECT * FROM retail limit 10;

-- Q2 Check # of records
select COUNT(*) as "Records Count" from retail;

-- Q3 number of clients (e.g. unique client ID)
select COUNT(distinct customer_id ) as "Number of Clients" from retail;

-- Q4 invoice date range (e.g. max/min dates)
select MAX(invoice_date)::TIMESTAMP(0) as "max", MIN(invoice_date)::TIMESTAMP(0) as "min"  from retail;

-- Q5 number of SKU/merchants (e.g. unique stock code)
select COUNT(distinct stock_code ) as "Number of SKU/merchants" from retail;

-- Q6 Calculate average invoice amount excluding invoices with a negative amount (e.g. canceled orders have negative amount)
select AVG(invoice_amount) as avg_valid_invoice_amount
from (
    select invoice_no,
           sum(unit_price * quantity) as invoice_amount
    from retail
    group by invoice_no
    having sum(unit_price * quantity) > 0
) valid_invoices;

-- Q7 Calculate total revenue (e.g. sum of unit_price * quantity)
select SUM(unit_price*quantity) from retail;

--Q8 Calculate total revenue by YYYYMM 
select TO_CHAR(invoice_date, 'YYYYMM') as date, SUM(unit_price*quantity)
from retail r
group by TO_CHAR(invoice_date, 'YYYYMM')
order by date;


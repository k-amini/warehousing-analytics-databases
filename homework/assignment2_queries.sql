--- Get the top 3 most profitable product types
SELECT product_line, sum(profit)
FROM products
INNER JOIN measures
ON products.product_code = measures.product_code
GROUP BY product_line
ORDER BY sum(profit) DESC
LIMIT(3);

--- Get the top 3 products by most items sold

SELECT products.product_code, product_name, sum(quantity_ordered)
FROM products
INNER JOIN measures
ON products.product_code = measures.product_code
GROUP BY products.product_code
ORDER BY sum(quantity_ordered) DESC
LIMIT(3);

--- Get the top 3 products by items sold per country of customer for: USA, Spain, Belgium

(select p.product_name as Most_sold_products_country, c.country, sum(quantity_ordered) AS Orders
	from products as p
	join measures as m
	on m.product_code = p.product_code
	join customers as c
	on m.customer_number = c.customer_number
	where country = 'USA'
	group by product_name, country
	order by sum(quantity_ordered) desc
	limit(3))
union all
(select p.product_name as Most_sold_products_country, c.country, sum(quantity_ordered) AS Orders
	from products as p
	join measures as m
	on m.product_code = p.product_code
	join customers as c
	on m.customer_number = c.customer_number
	where country = 'Spain'
	group by product_name, country
	order by sum(quantity_ordered) desc
	limit(3))
union all
(select p.product_name as Most_sold_products_country, c.country, sum(quantity_ordered) AS Orders
	from products as p
	join measures as m
	on m.product_code = p.product_code
	join customers as c
	on m.customer_number = c.customer_number
	where country = 'Belgium'
	group by product_name, country
	order by sum(quantity_ordered) desc
	limit(3));

--- Get the most profitable day of the week

SELECT sum(profit) AS total_profit, order_date_time.day
FROM order_date_time
INNER JOIN measures
ON order_date_time.order_date = measures.order_date
GROUP BY day
ORDER BY sum(profit) DESC
LIMIT(1);

--- Get the top 3 city-quarters with highest average profit margin

SELECT avg(margin), offices.city, order_date_time.quarter
FROM order_date_time
INNER JOIN measures
ON order_date_time.order_date = measures.order_date
INNER JOIN offices
ON measures.office_code = offices.office_code
GROUP BY offices.city, order_date_time.quarter
ORDER BY avg(margin) DESC
LIMIT(3);

-- List the employees who have sold more goods (in $ amount) than the average employee.

SELECT e.employee_number as MVE, sum(revenue) AS revenue
FROM employees as e
JOIN measures as m
ON e.employee_number = m.sales_rep_employee_number
GROUP BY e.employee_number
HAVING sum(revenue) >
  (SELECT sum(revenue)/COUNT(DISTINCT e.employee_number)
      FROM employees as e
      JOIN measures as m
      ON e.employee_number = m.sales_rep_employee_number
    );

-- List all the orders where the sales amount in the order is in the top 10% of all order sales amounts (BONUS: Add the employee number)

select order_number, sum(revenue) as revenue, max(sales_rep_employee_number) as employee_number
	from measures as m
	group by order_number
	order by sum(revenue) desc
	limit(select (count(*)  /10) from orders);

USE FOOD_DELIVERY;

/* 1. Annual Top Customers: This view returns the First Name, Last Name, Total Order
Amount of the customers who paid top 3 total amount of orders (in terms of total
balance in the orders) in past 1 year. */

CREATE VIEW ANNUAL_TOP_CUSTOMERS
AS
SELECT p.first_name, p.last_name, SUM(ord.total) total_order_amount
FROM PERSON AS p
	INNER JOIN CUSTOMER c
	ON p.person_id = c.customer_id
	INNER JOIN ORDERS ord
	ON c.customer_id = ord.customer_id
WHERE ord.order_date >= DATE_SUB(curdate(), INTERVAL 1 YEAR)
GROUP BY c.customer_id
ORDER BY total_order_amount DESC
LIMIT 3;


/* 2. Popular Restaurant Type: This view returns the Type of restaurants that have the most
number of orders in past 1 year */ 

CREATE VIEW POPULAR_RESTAURANT_TYPE
AS
SELECT styp.shop_type, COUNT(*) order_count, SUM(ord.total) total_order_amount
FROM ORDERS AS ord
	INNER JOIN RESTAURANT res
	ON ord.shop_id = res.shop_id
    INNER JOIN SHOP_TYPE styp
    ON ord.shop_id = styp.shop_id
WHERE ord.order_date >= DATE_SUB(curdate(), INTERVAL 1 YEAR)
GROUP BY styp.shop_type
ORDER BY order_count DESC; 

-- ALTERNATE -- 

-- SELECT ord.shop_id, restype.shop_type, COUNT(*) order_count
-- FROM ORDERS ord
-- INNER JOIN (SELECT res.shop_id, styp.shop_type 
-- FROM RESTAURANT res
-- INNER JOIN SHOP_TYPE styp
-- ON res.shop_id = styp.shop_id) restype
-- ON ord.shop_id = restype.shop_id
-- WHERE ord.order_date >= DATE_SUB(curdate(), INTERVAL 1 YEAR)
-- GROUP BY ord.shop_id
-- ORDER BY order_count DESC; 


/* 3. Potential Silver Member: This view returns the information of the customers (not a
silver member yet) who have placed orders more than 10 times in the past 1 month */ 

CREATE VIEW POTENTIAL_SILVER_MEMBER
AS
SELECT ord.customer_id, COUNT(*) AS order_count
FROM ORDERS ord 
	INNER JOIN ( 
		SELECT customer_id 
        FROM CUSTOMER 
        WHERE customer_id NOT IN (
			SELECT silver_customer_id
            FROM SILVER_CUSTOMER
        )
    ) nsm
    ON ord.customer_id = nsm.customer_id 
WHERE ord.order_date >= DATE_SUB(curdate(), INTERVAL 1 MONTH)
GROUP BY ord.customer_id
HAVING order_count >= 10
ORDER BY order_count DESC;


/* 4. Best Area Manager: This view returns the information of the area manager who
successfully made the most number of contracts with shops in her/his working area in
past 1 year */ 

CREATE VIEW CONTRACTS_IN_AREA_MANAGER_AREA
AS
SELECT con.area_manager_id, am.area, COUNT(*) total_contracts
FROM CONTRACT AS con
	INNER JOIN AREA_MANAGER am
    ON con.area_manager_id = am.area_manager_id
    INNER JOIN SHOP sh
    ON con.shop_id = sh.shop_id
WHERE am.area = sh.area AND con.start_time >= DATE_SUB(curdate(), INTERVAL 1 YEAR)
GROUP BY con.area_manager_id
ORDER BY total_contracts DESC;

CREATE VIEW BEST_AREA_MANAGER
AS
SELECT a.area_manager_id, a.area, a.total_contracts
FROM CONTRACTS_IN_AREA_MANAGER_AREA as a
WHERE (	SELECT COUNT(*) 
        FROM CONTRACTS_IN_AREA_MANAGER_AREA as b
        WHERE b.area = a.area AND b.total_contracts >= a.total_contracts) <= 1;


/* 5. Top Restaurants: This view returns the top restaurant that have the most orders in past 1
month for each restaurant type */ 


CREATE VIEW POPULAR_RESTAURANT_TYPE_MONTH
AS
SELECT ord.shop_id, styp.shop_type, COUNT(*) order_count
FROM ORDERS AS ord
	INNER JOIN RESTAURANT res
	ON ord.shop_id = res.shop_id
    INNER JOIN SHOP_TYPE styp
    ON ord.shop_id = styp.shop_id
WHERE ord.order_date >= DATE_SUB(curdate(), INTERVAL 1 MONTH)
GROUP BY ord.shop_id,  styp.shop_type
ORDER BY order_count DESC; 

CREATE VIEW TOP_RESTAURANTS
AS
SELECT a.shop_id, a.shop_type, a.order_count
FROM POPULAR_RESTAURANT_TYPE_MONTH as a
WHERE (	SELECT COUNT(*) 
        FROM POPULAR_RESTAURANT_TYPE_MONTH as b
        WHERE b.shop_type = a.shop_type AND b.order_count >= a.order_count ) <= 1;









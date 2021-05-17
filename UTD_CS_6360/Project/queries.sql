/* 1. Find the names of employee who supervises the most number of deliverers */ 


SELECT p.first_name, p.person_id, COUNT(*) total_deliverers_supervised
FROM PERSON AS p
	INNER JOIN AREA_MANAGER am
    ON p.person_id = am.area_manager_id
    INNER JOIN DELIVERER d
    ON am.area_manager_id = d.supervisor_id
GROUP BY am.area_manager_id
ORDER BY total_deliverers_supervised DESC;


/* 2. Find the average number of orders placed by Potential Silver Member. */ 



SELECT AVG(order_count) 'Average Number of Orders'
FROM POTENTIAL_SILVER_MEMBER;



/* 3. Find all the customers who placed orders of the restaurants that belong to Popular
Restaurant Type. Please also report the name of restaurants */ 


SELECT ord.customer_id, ord.shop_id, styp.shop_type
FROM ORDERS ord
	INNER JOIN SHOP_TYPE styp
    ON ord.shop_id = styp.shop_id
	INNER JOIN POPULAR_RESTAURANT_TYPE prt
    ON styp.shop_type = prt.shop_type
GROUP BY ord.customer_id, ord.shop_id;

-- FOR ONLY CUSTOMERS --  

SELECT ord.customer_id
FROM ORDERS ord
	INNER JOIN SHOP_TYPE styp
    ON ord.shop_id = styp.shop_id
	INNER JOIN POPULAR_RESTAURANT_TYPE prt
    ON styp.shop_type = prt.shop_type
GROUP BY ord.customer_id;



/* 4. List all the customers that have become a silver member within a month of joining the system. */ 




SELECT cust.customer_id, cust.join_date, ca.issue_date
FROM CARD AS ca
	INNER JOIN CUSTOMER cust
	ON ca.silver_customer_id = cust.customer_id
WHERE cust.join_date >= DATE_SUB(ca.issue_date, INTERVAL 1 MONTH);





/*5. Find the names of deliverers who delivered the most orders in past 1 month */ 


SELECT p.first_name, d.deliverer_id, COUNT(*) AS total_orders_delivered
FROM DELIVERY d
	INNER JOIN ORDERS ord
    ON ord.order_id = d.order_id
    INNER JOIN PERSON p
    ON p.person_id = d.deliverer_id
WHERE ord.order_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
GROUP BY d.deliverer_id
ORDER BY total_orders_delivered DESC;


/* 6. Find the restaurants that provide the most promotion in the past 1 month.  */ 

SELECT res.shop_id, COUNT(*) number_of_promos
FROM RESTAURANT res
	INNER JOIN PROMOTION promo
	ON res.shop_id = promo.shop_id
WHERE promo.start_date > DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
GROUP BY res.shop_id
ORDER BY number_of_promos DESC;

/* 7. Find the customer who have place orders of all Fast Food restaurants.  */ 


SELECT csu.customer_id, COUNT(*) fast_food_restaurant_orders
FROM (SELECT DISTINCT ord.customer_id, ord.shop_id
		FROM ORDERS AS ord
			INNER JOIN RESTAURANT res
			ON ord.shop_id = res.shop_id
			INNER JOIN SHOP_TYPE st
			ON st.shop_id = res.shop_id
		WHERE st.shop_type = 'Fast Food'
		GROUP BY ord.customer_id, ord.shop_id) csu
GROUP BY csu.customer_id
HAVING fast_food_restaurant_orders = (SELECT COUNT(*) fast_food_restaurant_count
										FROM SHOP_TYPE 
										WHERE shop_type = 'Fast Food');




/* 8. For each restaurant, list all the customers who placed the order, and the price of each order */ 


SELECT res.shop_id, ord.customer_id, ord.total
FROM ORDERS AS ord
	INNER JOIN RESTAURANT res
	ON ord.shop_id = res.shop_id;



/* 9. Find the area that have the most number of restaurants located. */ 


SELECT sh.area, COUNT(*) restaurant_count
FROM SHOP AS sh
	INNER JOIN RESTAURANT res
	ON sh.shop_id = res.shop_id
GROUP BY sh.area
ORDER BY restaurant_count DESC;


/* 10. Find the schedule of the restaurant that have the most orders in past 1 month */ 


SELECT sc.shop_id, sc.open_time, sc.close_time, sc.day_of_week, mo.order_count
FROM SCHEDULE AS sc
INNER JOIN (
		SELECT ord.shop_id, styp.shop_type, COUNT(*) order_count
		FROM ORDERS AS ord
			INNER JOIN RESTAURANT res
			ON ord.shop_id = res.shop_id
			INNER JOIN SHOP_TYPE styp
			ON ord.shop_id = styp.shop_id
		WHERE ord.order_date > DATE_SUB(CURDATE(), INTERVAL 1 MONTH) 
		GROUP BY ord.shop_id,  styp.shop_type
		ORDER BY order_count DESC
        LIMIT 1
	) mo
    ON sc.shop_id = mo.shop_id;




/* 11. Find the names of employee who are also a Gold Member. */ 


SELECT p.first_name, p.last_name, emp.employee_id, gc.gold_id
FROM GOLD_CUSTOMER AS gc
	INNER JOIN EMPLOYEE emp
	ON gc.gold_id = emp.gold_id
	INNER JOIN PERSON p
	ON emp.employee_id = p.person_id;




/* 12. Find the supermarket that have most different products in stock.  */ 


SELECT usp.shop_id, COUNT(*) product_count
FROM (SELECT shop_id, product_id
		FROM SALE 
		WHERE stock > 0
		GROUP BY shop_id, product_id) AS usp
GROUP BY usp.shop_id
ORDER BY product_count DESC
LIMIT 1;



/* 13. For each product, list all the supermarket selling it, and the price of the product at the supermarket. */ 


SELECT p.product_name, p.product_id, sup.shop_id, sal.price
FROM SALE AS sal
	INNER JOIN PRODUCT p
	ON sal.product_id = p.product_id
	INNER JOIN SUPERMARKET sup
	ON sal.shop_id = sup.shop_id;







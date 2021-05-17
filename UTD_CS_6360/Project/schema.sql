DROP SCHEMA IF EXISTS FOOD_DELIVERY;
CREATE SCHEMA FOOD_DELIVERY;

USE FOOD_DELIVERY;

DROP TABLE IF EXISTS PERSON;
CREATE TABLE IF NOT EXISTS PERSON (
  person_id int(11) NOT NULL AUTO_INCREMENT,
  first_name varchar(60) NOT NULL,
  middle varchar(60) NOT NULL,
  last_name varchar(60) NOT NULL,
  contact bigint(11) NOT NULL,
  address varchar(300) NOT NULL,
  PRIMARY KEY (person_id)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS CUSTOMER;
CREATE TABLE IF NOT EXISTS CUSTOMER (
  customer_id int(11) NOT NULL AUTO_INCREMENT,
  join_date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (customer_id),
  CONSTRAINT customer_person FOREIGN KEY (customer_id) REFERENCES PERSON(person_id)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS EMPLOYEE;
CREATE TABLE IF NOT EXISTS EMPLOYEE (
  employee_id int(11) NOT NULL AUTO_INCREMENT,
  gold_id bigint(11),
  work_id varchar(5) NOT NULL,
  age int(4) NOT NULL,
  PRIMARY KEY (employee_id),
  CONSTRAINT employee_person FOREIGN KEY (employee_id) REFERENCES PERSON(person_id)   
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;

DROP TRIGGER IF EXISTS trig_age_emp_check;
DELIMITER $$
CREATE TRIGGER trig_age_emp_check BEFORE INSERT ON EMPLOYEE
FOR EACH ROW 
BEGIN 
IF (NEW.age > 16) = 0 THEN 
  SIGNAL SQLSTATE '12345'
     SET MESSAGE_TEXT = 'Wroooong AGE!!!';
END IF; 

IF (NEW.work_id REGEXP 'E[0-9]{3}') = 0 THEN 
  SIGNAL SQLSTATE '12345'
     SET MESSAGE_TEXT = 'Wroooong Work ID!!!';
END IF; 

END$$
DELIMITER ;


DROP TABLE IF EXISTS GOLD_CUSTOMER;
CREATE TABLE IF NOT EXISTS GOLD_CUSTOMER (
  gold_id int(11) NOT NULL AUTO_INCREMENT,
  customer_id int(11) NOT NULL,
  pass_no int(11) NOT NULL,
  free_deliveries int(5) NOT NULL,
  PRIMARY KEY (gold_id),
  CONSTRAINT gold_customer_customer FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS SILVER_CUSTOMER;
CREATE TABLE IF NOT EXISTS SILVER_CUSTOMER (
  silver_customer_id int(11) NOT NULL,
  gold_id int(11),
  PRIMARY KEY (silver_customer_id),
  CONSTRAINT silver_customer_customer FOREIGN KEY (silver_customer_id) REFERENCES CUSTOMER(customer_id),
  CONSTRAINT silver_customer_gold_customer FOREIGN KEY (gold_id) REFERENCES GOLD_CUSTOMER(gold_id)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS ORDINARY_CUSTOMER;
CREATE TABLE IF NOT EXISTS ORDINARY_CUSTOMER (
  ordinary_customer_id int(11) NOT NULL,
  PRIMARY KEY (ordinary_customer_id),
  CONSTRAINT ordinary_customer_customer FOREIGN KEY (ordinary_customer_id) REFERENCES CUSTOMER(customer_id)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS EMPLOYMENT;
CREATE TABLE IF NOT EXISTS EMPLOYMENT (
  employment_id int(11) NOT NULL AUTO_INCREMENT,
  employee_id int(11) NOT NULL,
  start_date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  employee_role varchar(60) NOT NULL,
  PRIMARY KEY (employment_id),
  CONSTRAINT employment_employee FOREIGN KEY (employee_id) REFERENCES EMPLOYEE(employee_id)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS AREA_MANAGER;
CREATE TABLE IF NOT EXISTS AREA_MANAGER (
  area_manager_id int(11) NOT NULL,
  area varchar(60) NOT NULL,
  PRIMARY KEY (area_manager_id),
  CONSTRAINT area_manager_employee FOREIGN KEY (area_manager_id) REFERENCES EMPLOYEE(employee_id)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS DELIVERER;
CREATE TABLE IF NOT EXISTS DELIVERER (
  deliverer_id int(11) NOT NULL ,
  supervisor_id int(11) NOT NULL,
  PRIMARY KEY (deliverer_id),
  CONSTRAINT deliverer_employee FOREIGN KEY (deliverer_id) REFERENCES EMPLOYEE(employee_id),
  CONSTRAINT deliverer_area_manager FOREIGN KEY (supervisor_id) REFERENCES AREA_MANAGER(area_manager_id)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS STAFF;
CREATE TABLE IF NOT EXISTS STAFF (
  staff_id int(11) NOT NULL,
  PRIMARY KEY (staff_id),
  CONSTRAINT staff_employee FOREIGN KEY (staff_id) REFERENCES EMPLOYEE(employee_id)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS CARD;
CREATE TABLE IF NOT EXISTS CARD (
  silver_customer_id int(11) NOT NULL,
  staff_id int(11) NOT NULL,
  issue_date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (silver_customer_id, staff_id),
  CONSTRAINT card_silver_customer FOREIGN KEY (silver_customer_id) REFERENCES SILVER_CUSTOMER(silver_customer_id),
  CONSTRAINT card_staff FOREIGN KEY (staff_id) REFERENCES STAFF(staff_id)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS SHOP;
CREATE TABLE IF NOT EXISTS SHOP (
  shop_id int(11) NOT NULL AUTO_INCREMENT,
  shop_name varchar(60) NOT NULL,
  address varchar(60) NOT NULL,
  area varchar(60) NOT NULL,
  phone bigint(11) NOT NULL,
  PRIMARY KEY (shop_id)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS PROMOTION;
CREATE TABLE IF NOT EXISTS PROMOTION (
  shop_id int(11) NOT NULL,
  promotion_code varchar(20) NOT NULL,
  start_date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  description varchar(60) NOT NULL,
  PRIMARY KEY (promotion_code, shop_id),
  CONSTRAINT promotion_shop FOREIGN KEY (shop_id) REFERENCES SHOP(shop_id)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS ORDERS;
CREATE TABLE IF NOT EXISTS ORDERS (
  order_id int(11) NOT NULL AUTO_INCREMENT,
  customer_id int(11) NOT NULL,
  shop_id int(11) NOT NULL,
  promotion_code varchar(20) NULL,
  total int(11) NOT NULL,
  contents varchar(60) NOT NULL,
  order_date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (order_id),
  CONSTRAINT order_customer FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id),
  CONSTRAINT order_code FOREIGN KEY (promotion_code) REFERENCES PROMOTION(promotion_code),
  CONSTRAINT order_shop FOREIGN KEY (shop_id) REFERENCES SHOP(shop_id)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS CONTRACT;
CREATE TABLE IF NOT EXISTS CONTRACT (
  area_manager_id int(11) NOT NULL,
  shop_id int(11) NOT NULL,
  start_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (area_manager_id, shop_id),
  CONSTRAINT contract_area_manager FOREIGN KEY (area_manager_id) REFERENCES AREA_MANAGER(area_manager_id),
  CONSTRAINT contract_shop FOREIGN KEY (shop_id) REFERENCES SHOP(shop_id)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS VEHICLE;
CREATE TABLE IF NOT EXISTS VEHICLE (
  vehicle_id int(11) NOT NULL AUTO_INCREMENT,
  deliverer_id int(11) NOT NULL,
  model varchar(60) NOT NULL,
  plate_no bigint(11) NOT NULL,
  color varchar(60) NOT NULL,
  maker varchar(60) NOT NULL,
  PRIMARY KEY (vehicle_id),
  CONSTRAINT vehicle_deliverer FOREIGN KEY (deliverer_id) REFERENCES DELIVERER(deliverer_id)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS DELIVERY;
CREATE TABLE IF NOT EXISTS DELIVERY (
  order_id int(11) NOT NULL,
  deliverer_id int(11) NOT NULL,
  vehicle_id int(11) NOT NULL,
  PRIMARY KEY (order_id),
  CONSTRAINT delivery_deliverer FOREIGN KEY (deliverer_id) REFERENCES DELIVERER(deliverer_id),
  CONSTRAINT delivery_order FOREIGN KEY (order_id) REFERENCES ORDERS(order_id),
  CONSTRAINT delivery_vehicle FOREIGN KEY (vehicle_id) REFERENCES VEHICLE(vehicle_id)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS COMMENTS;
CREATE TABLE IF NOT EXISTS COMMENTS (
  customer_id int(11) NOT NULL,
  shop_id int(11) NOT NULL,
  rating enum('1','2','3','4','5') NOT NULL,
  comment varchar(60) NOT NULL,
  PRIMARY KEY (customer_id, shop_id),
  CONSTRAINT comments_customer FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id),
  CONSTRAINT comments_shop FOREIGN KEY (shop_id) REFERENCES SHOP(shop_id)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS PAYMENT;
CREATE TABLE IF NOT EXISTS PAYMENT (
  order_id int(11) NOT NULL,
  shop_id int(11) NOT NULL,
  confirmation varchar(60) NOT NULL,
  type varchar(60) NOT NULL,
  payment_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (order_id),
  CONSTRAINT payments_order FOREIGN KEY (order_id) REFERENCES ORDERS(order_id),
  CONSTRAINT payments_shop FOREIGN KEY (shop_id) REFERENCES SHOP(shop_id)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS RESTAURANT;
CREATE TABLE IF NOT EXISTS RESTAURANT (
  shop_id int(11) NOT NULL,
  PRIMARY KEY (shop_id),
  CONSTRAINT restaurant_shop FOREIGN KEY (shop_id) REFERENCES SHOP(shop_id)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS SUPERMARKET;
CREATE TABLE IF NOT EXISTS SUPERMARKET (
  shop_id int(11) NOT NULL,
  PRIMARY KEY (shop_id),
  CONSTRAINT supermarket_shop FOREIGN KEY (shop_id) REFERENCES SHOP(shop_id)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS PRODUCT;
CREATE TABLE IF NOT EXISTS PRODUCT (
  product_id int(11) NOT NULL,
  product_name varchar(50) NOT NULL,
  PRIMARY KEY (product_id)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS SHOP_TYPE;
CREATE TABLE IF NOT EXISTS SHOP_TYPE (
  shop_id int(11) NOT NULL,
  shop_type varchar(30) NOT NULL,
  PRIMARY KEY (shop_id, shop_type),
  CONSTRAINT shop_type_shop FOREIGN KEY (shop_id) REFERENCES SHOP(shop_id)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS SCHEDULE;
CREATE TABLE IF NOT EXISTS SCHEDULE (
  shop_id int(11) NOT NULL,
  day_of_week varchar(60) NOT NULL,
  open_time int(11) NOT NULL DEFAULT 0,
  close_time int(11) NOT NULL DEFAULT 24,
  PRIMARY KEY (shop_id, day_of_week),
  CONSTRAINT schedule_shop FOREIGN KEY (shop_id) REFERENCES SHOP(shop_id)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS SALE;
CREATE TABLE IF NOT EXISTS SALE (
  shop_id int(11) NOT NULL,
  product_id int(11) NOT NULL,
  stock varchar(60) NOT NULL,
  price varchar(60) NOT NULL,
  PRIMARY KEY (shop_id, product_id),
  CONSTRAINT sale_shop FOREIGN KEY (shop_id) REFERENCES SHOP(shop_id),
  CONSTRAINT sale_product FOREIGN KEY (product_id) REFERENCES PRODUCT(product_id)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;


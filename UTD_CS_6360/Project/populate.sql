USE FOOD_DELIVERY;

INSERT INTO PERSON VALUES (1, "John", "M", "Doe", 18762454865, "243 Concorde Rd Richardson TX");
INSERT INTO PERSON VALUES (2, "Bill", "H", "Clinton", 19362454864, "12 Wharton Rd Richardson TX");
INSERT INTO PERSON VALUES (3, "Jennifer", "C", "Lopez", 18276498560, "727 Potato Rd Richardson TX");
INSERT INTO PERSON VALUES (4, "Daenerys", "D", "Targaryen", 18375642967, "147 Dragon Rd Richardson TX");
INSERT INTO PERSON VALUES (5, "Jon", "B", "Snow", 19786548775, "155 Stark Rd Richardson TX");
INSERT INTO PERSON VALUES (6, "White", "M", "Walker", 18097654765, "790 Ice Rd Richardson TX");

INSERT INTO PERSON VALUES (7, "Khal", "K", "Drogo", 18273645678, "736 Horse Rd Plano TX");
INSERT INTO PERSON VALUES (8, "Arya", "K", "Stark", 18273647161, "117 Knife Rd Plano TX");
INSERT INTO PERSON VALUES (9, "Tyrion", "L", "Lannister", 18555545678, "969 Wine Rd Plano TX");

INSERT INTO CUSTOMER VALUES (1, "2001-12-03");
INSERT INTO CUSTOMER VALUES (2, "2002-11-13");
INSERT INTO CUSTOMER VALUES (3, "2002-07-14");
INSERT INTO CUSTOMER VALUES (4, "2003-10-10");
INSERT INTO CUSTOMER VALUES (9, "2010-11-12");

INSERT INTO ORDINARY_CUSTOMER VALUES (2);
INSERT INTO ORDINARY_CUSTOMER VALUES (9);

INSERT INTO GOLD_CUSTOMER VALUES (1, 3, 1111, 8);
INSERT INTO GOLD_CUSTOMER VALUES (2, 4, 1112, 6);

INSERT INTO SILVER_CUSTOMER VALUES(1, NULL);
INSERT INTO SILVER_CUSTOMER VALUES(3, 1);
INSERT INTO SILVER_CUSTOMER VALUES(4, 2);

INSERT INTO EMPLOYEE VALUES (4, 2, 'E004', 34);
INSERT INTO EMPLOYEE VALUES (5, NULL, 'E005', 32);
INSERT INTO EMPLOYEE VALUES (6, NULL, 'E006', 60);
INSERT INTO EMPLOYEE VALUES (7, NULL, 'E007', 38);
INSERT INTO EMPLOYEE VALUES (8, NULL, 'E008', 22);

INSERT INTO AREA_MANAGER VALUES (4, "Richardson");
INSERT INTO AREA_MANAGER VALUES (7, "Plano");

INSERT INTO DELIVERER VALUES (5, 4);
INSERT INTO DELIVERER VALUES (8, 7);

INSERT INTO STAFF VALUES (6);

INSERT INTO EMPLOYMENT VALUES (1, 4, "20100712", "Area Manager");
INSERT INTO EMPLOYMENT VALUES (2, 5, "20190617", "Deliverer");
INSERT INTO EMPLOYMENT VALUES (3, 6, "20050110", "Staff");
INSERT INTO EMPLOYMENT VALUES (4, 7, "20120307", "Area Manager");
INSERT INTO EMPLOYMENT VALUES (5, 8, "20200101", "Deliverer");

INSERT INTO CARD VALUES (1, 6, "2004-12-03");
INSERT INTO CARD VALUES (3, 6, "2002-08-10");
INSERT INTO CARD VALUES (4, 6, "2003-11-07");

INSERT INTO SHOP VALUES (1, "KFC", "142 Meat Rd Richardson TX", "Richardson", 16957387456);
INSERT INTO SHOP VALUES (2, "Burger King", "114 Dough Rd Richardson TX", "Richardson", 16388890768);
INSERT INTO SHOP VALUES (3, "Grills", "456 Smoke Rd Richardson TX", "Richardson", 16786542987);
INSERT INTO SHOP VALUES (4, "Rock Cafe", "711 Wine Rd Plano TX", "Plano", 16729837645);

INSERT INTO SHOP VALUES (5, "Target", "424 Crate Rd Richardson TX", "Richardson", 16827097856);
INSERT INTO SHOP VALUES (6, "Buckys", "765 Taco Rd Plano TX", "Plano", 16789457630);

INSERT INTO SHOP VALUES (7, "Rock Cafe1", "711 Wine Rd Plano TX", "Plano", 16729837646);
INSERT INTO SHOP VALUES (8, "Rock Cafe2", "711 Wine Rd Plano TX", "Plano", 16729837647);
INSERT INTO SHOP VALUES (9, "Rock Cafe3", "711 Wine Rd Plano TX", "Plano", 16729837648);
INSERT INTO SHOP VALUES (10, "Rock Cafe4", "711 Wine Rd Plano TX", "Plano", 16729837649);

INSERT INTO SHOP VALUES (11, "Buckys1", "765 Taco Rd Plano TX", "Plano", 16789457631);
INSERT INTO SHOP VALUES (12, "Buckys2", "765 Taco Rd Plano TX", "Plano", 16789457632);
INSERT INTO SHOP VALUES (13, "Buckys3", "765 Taco Rd Plano TX", "Plano", 16789457633);
INSERT INTO SHOP VALUES (14, "Buckys4", "765 Taco Rd Plano TX", "Plano", 16789457634);

INSERT INTO RESTAURANT VALUES (1);
INSERT INTO RESTAURANT VALUES (2);
INSERT INTO RESTAURANT VALUES (3);
INSERT INTO RESTAURANT VALUES (4);

INSERT INTO SUPERMARKET VALUES (5);
INSERT INTO SUPERMARKET VALUES (6);

INSERT INTO SHOP_TYPE VALUES (1, "Fast Food");
INSERT INTO SHOP_TYPE VALUES (2, "Fast Food");
INSERT INTO SHOP_TYPE VALUES (3, "BBQ");
INSERT INTO SHOP_TYPE VALUES (4, "Drink");

INSERT INTO SCHEDULE VALUES (1, "Monday", 8, 18);
INSERT INTO SCHEDULE VALUES (1, "Tuesday", 8, 18);
INSERT INTO SCHEDULE VALUES (1, "Wednesday", 8, 18);
INSERT INTO SCHEDULE VALUES (1, "Thursday", 8, 18);
INSERT INTO SCHEDULE VALUES (1, "Friday", 8, 14);

INSERT INTO SCHEDULE VALUES (2, "Monday", 8, 18);
INSERT INTO SCHEDULE VALUES (2, "Tuesday", 8, 18);
INSERT INTO SCHEDULE VALUES (2, "Wednesday", 8, 18);
INSERT INTO SCHEDULE VALUES (2, "Thursday", 8, 18);
INSERT INTO SCHEDULE VALUES (2, "Friday", 8, 14);

INSERT INTO SCHEDULE VALUES (3, "Monday", 8, 18);
INSERT INTO SCHEDULE VALUES (3, "Tuesday", 8, 18);
INSERT INTO SCHEDULE VALUES (3, "Wednesday", 8, 18);
INSERT INTO SCHEDULE VALUES (3, "Thursday", 8, 18);
INSERT INTO SCHEDULE VALUES (3, "Friday", 8, 14);

INSERT INTO SCHEDULE VALUES (4, "Monday", 8, 18);
INSERT INTO SCHEDULE VALUES (4, "Tuesday", 8, 18);
INSERT INTO SCHEDULE VALUES (4, "Wednesday", 8, 18);
INSERT INTO SCHEDULE VALUES (4, "Thursday", 8, 18);
INSERT INTO SCHEDULE VALUES (4, "Friday", 8, 14);

INSERT INTO SCHEDULE VALUES (5, "Monday", 8, 18);
INSERT INTO SCHEDULE VALUES (5, "Tuesday", 8, 18);
INSERT INTO SCHEDULE VALUES (5, "Wednesday", 8, 18);
INSERT INTO SCHEDULE VALUES (5, "Thursday", 8, 18);
INSERT INTO SCHEDULE VALUES (5, "Friday", 8, 14);

INSERT INTO SCHEDULE VALUES (6, "Monday", 8, 18);
INSERT INTO SCHEDULE VALUES (6, "Tuesday", 8, 18);
INSERT INTO SCHEDULE VALUES (6, "Wednesday", 8, 18);
INSERT INTO SCHEDULE VALUES (6, "Thursday", 8, 18);
INSERT INTO SCHEDULE VALUES (6, "Friday", 8, 14);

INSERT INTO PRODUCT VALUES (1, "Carrots");
INSERT INTO PRODUCT VALUES (2, "Beans");
INSERT INTO PRODUCT VALUES (3, "Soda");
INSERT INTO PRODUCT VALUES (4, "Chocolate");
INSERT INTO PRODUCT VALUES (5, "Toothbrush");

INSERT INTO SALE VALUES (5, 1, "30kg", "5$");
INSERT INTO SALE VALUES (5, 2, "25kg", "3$");
INSERT INTO SALE VALUES (5, 4, "5kg", "20$");
INSERT INTO SALE VALUES (6, 3, "20", "12$");
INSERT INTO SALE VALUES (6, 5, "15", "10$");

INSERT INTO CONTRACT VALUES (4, 1, "20200801");
INSERT INTO CONTRACT VALUES (4, 2, "20181001");
INSERT INTO CONTRACT VALUES (4, 3, "20160701");
INSERT INTO CONTRACT VALUES (4, 5, "20120101");

INSERT INTO CONTRACT VALUES (7, 4, "20191201");
INSERT INTO CONTRACT VALUES (7, 6, "20180601");

INSERT INTO VEHICLE VALUES (1, 5, "Veyron", 874639, "Red", "Bugatti");
INSERT INTO VEHICLE VALUES (2, 8, "Gallardo", 587468, "Yello", "Lamborghini");

INSERT INTO PROMOTION VALUES (1, "Offer20", "2021-04-03", "Get 20 percent off");
INSERT INTO PROMOTION VALUES (2, "Offer15", "2021-04-05", "Get 15 percent off");
INSERT INTO PROMOTION VALUES (2, "BuyOneGetOne", "2021-04-05", "Buy one and get one free");
INSERT INTO PROMOTION VALUES (3, "Offer10", "2021-04-04", "Get 10 percent off");
INSERT INTO PROMOTION VALUES (4, "Offer25", "2021-04-04", "Get 25 percent off");

INSERT INTO PROMOTION VALUES (5, "BuyOneGetOne", "2021-04-04", "Buy one and get one free");
INSERT INTO PROMOTION VALUES (6, "BuyOneGetOne", "2021-04-05", "Buy one and get one free");

INSERT INTO COMMENTS VALUES (3, 1, '5', "Food was excellent.");
INSERT INTO COMMENTS VALUES (2, 2, '2', "Food was not cooked properly.");
INSERT INTO COMMENTS VALUES (9, 6, '4', "Great service.");

INSERT INTO ORDERS VALUES (1, 2, 1, "Offer20", 18, "6 piece bucket", "2021-04-03");
INSERT INTO ORDERS VALUES (2, 2, 1, "Offer20", 18, "6 piece bucket", "2021-04-04");
INSERT INTO ORDERS VALUES (3, 2, 1, "Offer20", 12, "burger and fries", "2021-04-05");
INSERT INTO ORDERS VALUES (4, 2, 1, "Offer20", 24, "8 piece bucket", "2021-04-06");
INSERT INTO ORDERS VALUES (5, 2, 1, "Offer20", 12, "burger and fries", "2021-04-07");
INSERT INTO ORDERS VALUES (6, 2, 2, "Offer15", 20, "burger and fries", "2021-04-08");
INSERT INTO ORDERS VALUES (7, 2, 2, "Offer15", 8, "chicken wings", "2021-04-09");
INSERT INTO ORDERS VALUES (8, 2, 5, "BuyOneGetOne", 20, "Carrots", "2021-04-10");
INSERT INTO ORDERS VALUES (9, 2, 5, "BuyOneGetOne", 12, "Beans", "2021-04-11");
INSERT INTO ORDERS VALUES (10, 2, 5, "BuyOneGetOne", 20, "Carrots", "2021-04-12");
INSERT INTO ORDERS VALUES (11, 2, 5, "BuyOneGetOne", 40, "Chocolate", "2021-04-13");

INSERT INTO ORDERS VALUES (12, 1, 2, "Offer15", 20, "burger and fries", "2021-04-14");
INSERT INTO ORDERS VALUES (13, 1, 1, "Offer20", 18, "6 piece bucket", "2021-04-15");

INSERT INTO ORDERS VALUES (14, 3, 1, "Offer20", 18, "6 piece bucket", "2021-04-16");
INSERT INTO ORDERS VALUES (15, 3, 1, "Offer20", 24, "8 piece bucket", "2021-04-17");

INSERT INTO ORDERS VALUES (16, 4, 1, "Offer20", 18, "6 piece bucket", "2021-04-18");
INSERT INTO ORDERS VALUES (17, 4, 3, "Offer10", 30, "Chicken BBQ", "2021-04-19");

INSERT INTO ORDERS VALUES (18, 9, 4, "Offer25", 50, "Wine bottle", "2021-04-20");
INSERT INTO ORDERS VALUES (19, 9, 6, "BuyOneGetOne", 24, "4 cans of soda", "2021-04-21");
INSERT INTO ORDERS VALUES (20, 9, 6, "BuyOneGetOne", 20, "4 toothbrushes", "2021-04-22");

INSERT INTO ORDERS VALUES (21, 2, 5, "BuyOneGetOne", 40, "Banana", "2021-04-18");
INSERT INTO ORDERS VALUES (22, 2, 5, "BuyOneGetOne", 40, "Kiwi", "2021-04-19");

INSERT INTO PAYMENT VALUES (1, 1, "12345678", "Credit Card", "2021-04-01 13:00:00");
INSERT INTO PAYMENT VALUES (2, 1, "28726357", "Credit Card", "2021-04-02 13:04:00");
INSERT INTO PAYMENT VALUES (3, 1, "79827364", "Credit Card", "2021-04-03 13:02:00");
INSERT INTO PAYMENT VALUES (4, 1, "29837465", "Credit Card", "2021-04-04 13:03:00");
INSERT INTO PAYMENT VALUES (5, 1, "20938765", "Credit Card", "2021-04-05 13:04:00");
INSERT INTO PAYMENT VALUES (6, 2, "93847465", "Credit Card", "2021-04-06 13:05:00");
INSERT INTO PAYMENT VALUES (7, 2, "09876875", "Credit Card", "2021-04-07 13:06:00");
INSERT INTO PAYMENT VALUES (8, 5, "73629283", "Credit Card", "2021-04-08 13:07:00");
INSERT INTO PAYMENT VALUES (9, 5, "92837998", "Credit Card", "2021-04-09 13:08:00");
INSERT INTO PAYMENT VALUES (10, 5, "38790876", "Credit Card", "2021-04-10 13:09:00");
INSERT INTO PAYMENT VALUES (11, 5, "64738298", "Credit Card", "2021-04-11 13:10:00");

INSERT INTO PAYMENT VALUES (12, 2, "98765678", "Cash", "2021-04-12 14:00:00");
INSERT INTO PAYMENT VALUES (13, 1, "65435987", "Cash", "2021-04-13 14:30:00");

INSERT INTO PAYMENT VALUES (14, 1, "98765456", "Credit Card", "2021-04-14 13:50:00");
INSERT INTO PAYMENT VALUES (15, 1, "92837460", "Credit Card", "2021-04-15 13:30:00");

INSERT INTO PAYMENT VALUES (16, 1, "65267899", "Credit Card", "2021-04-16 14:00:00");
INSERT INTO PAYMENT VALUES (17, 3, "29837990", "Credit Card", "2021-04-17 15:00:00");

INSERT INTO PAYMENT VALUES (18, 4, "11009988", "Credit Card", "2021-04-18 13:15:00");
INSERT INTO PAYMENT VALUES (19, 6, "22887755", "Credit Card", "2021-04-19 13:30:00");
INSERT INTO PAYMENT VALUES (20, 6, "33887766", "Credit Card", "2021-04-20 13:40:00");

INSERT INTO DELIVERY VALUES (1, 5, 1);
INSERT INTO DELIVERY VALUES (2, 5, 1);
INSERT INTO DELIVERY VALUES (3, 5, 1);
INSERT INTO DELIVERY VALUES (4, 5, 1);
INSERT INTO DELIVERY VALUES (5, 5, 1);
INSERT INTO DELIVERY VALUES (6, 5, 1);
INSERT INTO DELIVERY VALUES (7, 5, 1);
INSERT INTO DELIVERY VALUES (8, 5, 1);
INSERT INTO DELIVERY VALUES (9, 5, 1);
INSERT INTO DELIVERY VALUES (10, 5, 1);
INSERT INTO DELIVERY VALUES (11, 5, 1);

INSERT INTO DELIVERY VALUES (12, 5, 1);
INSERT INTO DELIVERY VALUES (13, 5, 1);

INSERT INTO DELIVERY VALUES (14, 5, 1);
INSERT INTO DELIVERY VALUES (15, 5, 1);

INSERT INTO DELIVERY VALUES (16, 5, 1);
INSERT INTO DELIVERY VALUES (17, 5, 1);

INSERT INTO DELIVERY VALUES (18, 8, 2);
INSERT INTO DELIVERY VALUES (19, 8, 2);
INSERT INTO DELIVERY VALUES (20, 8, 2);
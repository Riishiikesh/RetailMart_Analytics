USE retailmart;



SELECT COUNT(*) FROM categories;
SELECT COUNT(*) FROM customers;
SELECT COUNT(*) FROM products;
SELECT COUNT(*) FROM sales_transactions;
SELECT COUNT(*) FROM sales_items;
SELECT COUNT(*) FROM vouchers;
SELECT COUNT(*) FROM voucher_redemptions;
SELECT COUNT(*) FROM returns;

SHOW VARIABLES LIKE 'local_infile';

SHOW VARIABLES LIKE 'secure_file_priv';

SHOW VARIABLES LIKE 'local_infile';







--        ---------------------------------------------------------------------------------------------------

LOAD DATA LOCAL INFILE "C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\categories.csv"
INTO TABLE categories
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(category_id, category_name, description);

SELECT COUNT(*) AS total_categories
FROM categories;


SELECT * FROM categories
LIMIT 10;


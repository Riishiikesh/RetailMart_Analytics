CREATE DATABASE retailmart;

USE retailmart;


 -- categories table
 
 CREATE TABLE categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    description TEXT
);

                    --  customers table

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(150),
    phone VARCHAR(20),
    city VARCHAR(100),
    registration_date DATE,
    loyalty_tier VARCHAR(20)
);

                         --  products table--
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category_id INT NOT NULL,
    unit_price DECIMAL(12,2) NOT NULL,
    cost_price DECIMAL(12,2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,

    CONSTRAINT fk_products_category
        FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
);
                      --  sales_transactions table
                      
CREATE TABLE sales_transactions (
    transaction_id INT PRIMARY KEY,
    customer_id INT NULL,
    store_id INT NOT NULL,
    transaction_date DATE NOT NULL,
    transaction_time TIME NOT NULL,
    payment_method VARCHAR(30) NOT NULL,
    total_amount DECIMAL(12,2) NOT NULL,
    discount_amount DECIMAL(12,2) DEFAULT 0,
    tax_amount DECIMAL(12,2) DEFAULT 0,
    net_amount DECIMAL(12,2) NOT NULL,

    CONSTRAINT fk_sales_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);

                          --  sales_items table
           
CREATE TABLE sales_items (
    item_id INT PRIMARY KEY,
    transaction_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(12,2) NOT NULL,
    line_total DECIMAL(12,2) NOT NULL,

    CONSTRAINT fk_items_transaction
        FOREIGN KEY (transaction_id)
        REFERENCES sales_transactions(transaction_id),

    CONSTRAINT fk_items_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);

                        -- vouchers table
                        
CREATE TABLE vouchers (
    voucher_id INT PRIMARY KEY,
    voucher_code VARCHAR(50) NOT NULL UNIQUE,
    voucher_type VARCHAR(20) NOT NULL,
    discount_value DECIMAL(12,2) NOT NULL,
    min_purchase_amount DECIMAL(12,2) NOT NULL,
    max_discount_amount DECIMAL(12,2),
    valid_from DATE NOT NULL,
    valid_to DATE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);


                 -- voucher_redemptions table
                 
                 
CREATE TABLE voucher_redemptions (
    redemption_id INT PRIMARY KEY,
    voucher_id INT NOT NULL,
    transaction_id INT NOT NULL,
    customer_id INT NOT NULL,
    redemption_date DATE NOT NULL,
    discount_applied DECIMAL(12,2) NOT NULL,

    FOREIGN KEY (voucher_id)
        REFERENCES vouchers(voucher_id),

    FOREIGN KEY (transaction_id)
        REFERENCES sales_transactions(transaction_id),

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);

                             -- returns table
                             
                             
CREATE TABLE returns (
    return_id INT PRIMARY KEY,
    transaction_id INT NOT NULL,
    item_id INT NOT NULL,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    return_date DATE NOT NULL,
    return_quantity INT NOT NULL,
    return_reason VARCHAR(100) NOT NULL,
    refund_amount DECIMAL(12,2) NOT NULL,
    refund_status VARCHAR(30) NOT NULL,

    FOREIGN KEY (transaction_id)
        REFERENCES sales_transactions(transaction_id),

    FOREIGN KEY (item_id)
        REFERENCES sales_items(item_id),

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);

SHOW TABLES;

SELECT COUNT(*) FROM categories;
SELECT COUNT(*) FROM customers;
SELECT COUNT(*) FROM products;
SELECT COUNT(*) FROM sales_transactions;
SELECT COUNT(*) FROM sales_items;
SELECT COUNT(*) FROM vouchers;
SELECT COUNT(*) FROM voucher_redemptions;
SELECT COUNT(*) FROM returns;





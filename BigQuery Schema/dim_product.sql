CREATE OR REPLACE TABLE
`retailmart-analytics-506321.retailmart_analytics.dim_product`
CLUSTER BY category_id
AS
SELECT
    p.product_id,
    p.product_name,
    p.category_id,
    c.category_name,
    p.unit_price,
    p.cost_price,
    p.stock_quantity,
    p.is_active
FROM
`retailmart-analytics-506321.retailmart_raw.products` p
LEFT JOIN
`retailmart-analytics-506321.retailmart_raw.categories` c
ON p.category_id = c.category_id;

----------------- ##Check--

SELECT COUNT(*) AS product_count
FROM
`retailmart-analytics-506321.retailmart_analytics.dim_product`;



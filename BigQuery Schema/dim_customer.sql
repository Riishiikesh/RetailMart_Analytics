CREATE OR REPLACE TABLE
`retailmart-analytics-506321.retailmart_analytics.dim_customer`
CLUSTER BY customer_id
AS
SELECT
    customer_id,
    first_name,
    last_name,
    email,
    phone,
    city,
    registration_date,
    loyalty_tier
FROM
`retailmart-analytics-506321.retailmart_raw.customers`;

------------------------------------ ##Chack

SELECT COUNT(*) AS customer_count
FROM
`retailmart-analytics-506321.retailmart_analytics.dim_customer`;



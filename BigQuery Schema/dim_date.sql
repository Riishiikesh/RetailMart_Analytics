CREATE OR REPLACE TABLE
`retailmart-analytics-506321.retailmart_analytics.dim_date`
AS
WITH all_dates AS (
    SELECT DATE(transaction_date) AS business_date
    FROM
    `retailmart-analytics-506321.retailmart_raw.sales_transactions`
    UNION ALL
    SELECT DATE(return_date) AS business_date
    FROM
    `retailmart-analytics-506321.retailmart_raw.returns`
),
date_range AS (
    SELECT
        MIN(business_date) AS min_date,
        MAX(business_date) AS max_date
    FROM all_dates
)
SELECT CAST(FORMAT_DATE('%Y%m%d', date_value) AS INT64) AS date_key,
    date_value AS full_date,
    EXTRACT(YEAR FROM date_value) AS year,
    EXTRACT(QUARTER FROM date_value) AS quarter,
    EXTRACT(MONTH FROM date_value) AS month,
    FORMAT_DATE('%B', date_value) AS month_name,
    EXTRACT(WEEK FROM date_value) AS week,
    EXTRACT(DAY FROM date_value) AS day,
    FORMAT_DATE('%A', date_value) AS day_name,
    EXTRACT(DAYOFWEEK FROM date_value)
        IN (1, 7) AS is_weekend
FROM date_range,

UNNEST(GENERATE_DATE_ARRAY(
        min_date,
        max_date
    )
) AS date_value;

---------------------------------- ## expected Output 
SELECT
    MIN(full_date) AS min_date,
    MAX(full_date) AS max_date,
    COUNT(*) AS total_days
FROM
`retailmart-analytics-506321.retailmart_analytics.dim_date`;





CREATE OR REPLACE TABLE
`retailmart-analytics-506321.retailmart_analytics.fact_returns`
AS
SELECT
    return_id,
    transaction_id,
    DATE(return_date) AS return_date,
    CAST(FORMAT_DATE('%Y%m%d',DATE(return_date)) AS INT64) AS date_key,
    product_id AS product_key,
    customer_id AS customer_key,
    return_quantity AS quantity_returned,
    CAST(refund_amount AS NUMERIC) AS refund_amount, return_reason, refund_status
FROM
`retailmart-analytics-506321.retailmart_raw.returns`;

------------------------------------------------------------ ##Check

SELECT COUNT(*) AS fact_returns_count
FROM
`retailmart-analytics-506321.retailmart_analytics.fact_returns`;


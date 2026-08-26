CREATE OR REPLACE TABLE
`retailmart-analytics-506321.retailmart_analytics.fact_sales`
AS
SELECT
    si.transaction_id,
    si.item_id,
    DATE(st.transaction_date) AS transaction_date,
    CAST(FORMAT_DATE('%Y%m%d',DATE(st.transaction_date)) AS INT64) AS date_key,
    si.product_id AS product_key,
    st.customer_id AS customer_key,
    st.store_id AS store_key,
    si.quantity,
    CAST(si.unit_price AS NUMERIC) AS unit_price,
    CAST(si.line_total AS NUMERIC) AS gross_revenue
FROM
`retailmart-analytics-506321.retailmart_raw.sales_items` si
JOIN
`retailmart-analytics-506321.retailmart_raw.sales_transactions` st
ON si.transaction_id = st.transaction_id;


------------------------------------------------------------ ##Chack


SELECT COUNT(*) AS fact_sales_count
FROM
`retailmart-analytics-506321.retailmart_analytics.fact_sales`;





CREATE OR REPLACE TABLE
`retailmart-analytics-506321.retailmart_analytics.dim_store`
CLUSTER BY store_id
AS
SELECT DISTINCT store_id, CONCAT('Store ', CAST(store_id AS STRING)) AS store_name
FROM
`retailmart-analytics-506321.retailmart_raw.sales_transactions`;

------------------------------------- ## Check

SELECT * FROM
`retailmart-analytics-506321.retailmart_analytics.dim_store`
ORDER BY store_id;



SELECT COUNT(*) AS store_count
FROM
`retailmart-analytics-506321.retailmart_analytics.dim_store`;


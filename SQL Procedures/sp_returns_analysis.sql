CREATE OR REPLACE PROCEDURE
`retailmart-analytics-506321.retailmart_analytics.sp_returns_analysis`(
    input_year INT64, input_month INT64
)
BEGIN
    WITH return_data AS (
        SELECT
            fr.return_id,
            fr.transaction_id,
            fr.product_key,
            fr.quantity_returned,
            fr.refund_amount
        FROM`retailmart-analytics-506321.retailmart_analytics.fact_returns` fr
        WHERE EXTRACT( YEAR FROM fr.return_date) = input_year
        AND EXTRACT(MONTH FROM fr.return_date ) = input_month
    ),
    return_by_category AS (
	SELECT
		dp.category_id,
		dp.category_name,
            COUNT(DISTINCT rd.return_id) AS total_returns,
            SUM(rd.quantity_returned) AS quantity_returned,
            SUM(rd.refund_amount) AS revenue_impact
        FROM return_data rd
        LEFT JOIN `retailmart-analytics-506321.retailmart_analytics.dim_product` dp
        ON rd.product_key = dp.product_id
        GROUP BY dp.category_id, dp.category_name
    ),
    sales_by_category AS (
        SELECT fs.product_key,
            SUM(fs.quantity) AS quantity_sold
        FROM `retailmart-analytics-506321.retailmart_analytics.fact_sales` fs
        WHERE EXTRACT(YEAR FROM fs.transaction_date) = input_year
        AND EXTRACT(MONTH FROM fs.transaction_date) = input_month
        GROUP BY fs.product_key
    ),
    category_sales AS (
        SELECT dp.category_id,
            SUM(sb.quantity_sold) AS quantity_sold
        FROM sales_by_category sb
        LEFT JOIN `retailmart-analytics-506321.retailmart_analytics.dim_product` dp
        ON sb.product_key = dp.product_id
        GROUP BY dp.category_id
    )
    SELECT
        r.category_id,
        r.category_name,
        r.total_returns,
        r.quantity_returned,
        COALESCE(s.quantity_sold, 0) AS quantity_sold,
        ROUND(SAFE_DIVIDE(r.quantity_returned, s.quantity_sold) * 100, 2) AS return_rate_percentage, r.revenue_impact
    FROM return_by_category r
    LEFT JOIN category_sales s
        ON r.category_id = s.category_id
    ORDER BY r.revenue_impact DESC;
END;



------ chechking

CALL `retailmart-analytics-506321.retailmart_analytics.sp_returns_analysis`(
    2023, 3
);



    
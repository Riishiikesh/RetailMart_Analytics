CREATE OR REPLACE PROCEDURE
`retailmart-analytics-506321.retailmart_analytics.sp_sales_metrics`(
    input_year INT64, input_month INT64
)
BEGIN
    DECLARE current_revenue NUMERIC DEFAULT 0;
    DECLARE previous_month_revenue NUMERIC DEFAULT 0;
    DECLARE previous_year_revenue NUMERIC DEFAULT 0;
    DECLARE mom_percentage NUMERIC;
    DECLARE yoy_percentage NUMERIC;
    
    -- Current month revenue
    
    SET current_revenue = (
        SELECT COALESCE(
                SUM(gross_revenue), 0
            )
        FROM `retailmart-analytics-506321.retailmart_analytics.fact_sales`
        WHERE EXTRACT(YEAR FROM transaction_date) = input_year
        AND EXTRACT(MONTH FROM transaction_date) = input_month
    );
    
    -- Previous month revenue

    SET previous_month_revenue = (
        SELECT COALESCE(SUM(gross_revenue), 0)
        FROM `retailmart-analytics-506321.retailmart_analytics.fact_sales`
        WHERE transaction_date >= DATE_SUB( DATE(input_year, input_month, 1), INTERVAL 1 MONTH)
        AND transaction_date < DATE(input_year, input_month, 1)
    );

    -- Same month previous year

    SET previous_year_revenue = (
SELECT COALESCE( SUM(gross_revenue), 0 )
        FROM `retailmart-analytics-506321.retailmart_analytics.fact_sales`
        WHERE transaction_date >= DATE(input_year - 1, input_month, 1)
        AND transaction_date < DATE(input_year - 1, input_month, 1) + INTERVAL 1 MONTH
    );
    -- MoM percentage

    SET mom_percentage = (
        CASE
        WHEN previous_month_revenue = 0
            THEN NULL
		ELSE ((current_revenue - previous_month_revenue) / previous_month_revenue) * 100
        END
    );

    -- YoY percentage

    SET yoy_percentage = (
        CASE
        WHEN previous_year_revenue = 0
            THEN NULL
		ELSE((current_revenue - previous_year_revenue) / previous_year_revenue) * 100
        END
    );

    SELECT input_year AS year, input_month AS month,
           current_revenue AS total_revenue, previous_month_revenue,
        ROUND(mom_percentage, 2) AS mom_percentage,
        previous_year_revenue,
        ROUND(yoy_percentage, 2) AS yoy_percentage;
END;

---------------------------- example chechking


CALL `retailmart-analytics-506321.retailmart_analytics.sp_sales_metrics`(
    2024, 2
);

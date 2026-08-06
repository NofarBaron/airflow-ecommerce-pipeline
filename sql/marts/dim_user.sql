CREATE OR REPLACE TABLE `my-project-284-493514.ecommerce_data.dim_user` AS

WITH event_summary AS (
    SELECT
        customer_id,
        MIN(event_time) AS first_seen,
        COUNT(*) AS total_events
    FROM `my-project-284-493514.ecommerce_data.fact_events`
    GROUP BY customer_id
),
order_summary AS (
    SELECT
        customer_id,
        SUM(order_amount) AS total_spent,
        COUNT(*) AS total_orders,
        SUM(
            CASE 
                WHEN LOWER(status) = 'success'
                THEN 1 
                ELSE 0 
            END
        ) AS success_orders,
        SUM(
            CASE 
                WHEN LOWER(status) = 'failed'
                THEN 1 
                ELSE 0 
            END
        ) AS failed_orders,
        SUM(
            CASE 
                WHEN LOWER(status) = 'refunded'
                THEN 1 
                ELSE 0 
            END
        ) AS refunded_orders
    FROM `my-project-284-493514.ecommerce_data.orders`
    GROUP BY customer_id
)
SELECT
    e.customer_id,
    e.first_seen,
    e.total_events,
    IF(o.customer_id IS NOT NULL, TRUE, FALSE) AS is_payer,
    COALESCE(o.total_spent,0) AS total_spent,
    COALESCE(o.total_orders,0) AS total_orders,
    COALESCE(o.success_orders,0) AS success_orders,
    COALESCE(o.failed_orders,0) AS failed_orders,
    COALESCE(o.refunded_orders,0) AS refunded_orders
FROM event_summary e
LEFT JOIN order_summary o
USING(customer_id)
;



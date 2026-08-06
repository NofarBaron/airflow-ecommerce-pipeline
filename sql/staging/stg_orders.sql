
CREATE OR REPLACE TABLE `my-project-284-493514.ecommerce_data.stg_orders` AS
SELECT
  order_id,
  customer_id,
  product_id,
  SAFE_CAST(order_amount AS FLOAT64) as order_amount,
  coalesce(SAFE_CAST(order_date AS TIMESTAMP),SAFE.PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', order_date)) AS order_time,
  payment_method,
  CASE
    WHEN LOWER(TRIM(status)) IN ('success', 'suc')
        THEN 'success'

    WHEN LOWER(TRIM(status)) IN ('failed', 'fail')
        THEN 'failed'

    WHEN LOWER(TRIM(status)) IN ('refunded', 'ref')
        THEN 'refunded'

    ELSE 'unknown'
  END AS status,
    COALESCE(SAFE_CAST(
            ABS(ROUND(SAFE_CAST(quantity AS FLOAT64)))
            AS INT64),1)
           AS quantity
FROM `my-project-284-493514.ecommerce_data.orders`
WHERE order_id IS NOT NULL
and order_date is not null 
and SAFE_CAST(order_amount AS FLOAT64) IS NOT NULL
;
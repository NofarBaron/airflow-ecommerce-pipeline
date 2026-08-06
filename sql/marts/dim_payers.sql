--create dim_payers
CREATE OR REPLACE TABLE `ecommerce_data.dim_payers` AS
SELECT
  customer_id,
  COUNT(*) AS total_orders,
  SUM(order_amount) AS total_revenue
FROM `ecommerce_data.stg_orders`
GROUP BY customer_id;
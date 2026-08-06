--create dim_sessions 
CREATE OR REPLACE TABLE `my-project-284-493514.ecommerce_data.dim_session` AS
SELECT
  session_id,
  customer_id,
  MIN(event_time) AS session_start,
  MAX(event_time) AS session_end,
  COUNT(*) AS events_in_session
FROM `my-project-284-493514.ecommerce_data.fact_events`
GROUP BY session_id, customer_id;
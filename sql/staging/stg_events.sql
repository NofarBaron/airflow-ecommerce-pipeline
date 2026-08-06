CREATE OR REPLACE TABLE `my-project-284-493514.ecommerce_data.stg_events` AS
SELECT
  event_id,
  session_id,
  customer_id,
  LOWER(event_type) AS event_type,
  page_url,
  device_id,
  coalesce(SAFE_CAST(timestamp AS TIMESTAMP),SAFE.PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', timestamp)) AS event_time,
  ingest_run_id
FROM `my-project-284-493514.ecommerce_data.events_sample`
WHERE event_id IS NOT NULL
and timestamp is not null 
;

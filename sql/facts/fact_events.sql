CREATE OR REPLACE TABLE `my-project-284-493514.ecommerce_data.fact_events` AS
SELECT *
FROM `my-project-284-493514.ecommerce_data.stg_events`
where event_time is not null;

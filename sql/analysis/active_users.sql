  #MAU
  SELECT DATE_TRUNC(DATE(event_time), MONTH) AS month,
    count(distinct customer_id) users 
  FROM `my-project-284-493514.ecommerce_data.fact_events`
  where customer_id is not null 
  and date(event_time)< date('2026-03-01')
  GROUP BY 1

  #DAU
    SELECT date(event_time) as event_date,
    count(distinct customer_id) users 
  FROM `my-project-284-493514.ecommerce_data.fact_events`
  where customer_id is not null 
  and date(event_time)< date('2025-12-04')
  GROUP BY 1
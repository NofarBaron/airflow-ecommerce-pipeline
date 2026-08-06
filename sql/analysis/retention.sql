#retention by week 
WITH first_seen AS (
  SELECT
    customer_id,
    DATE(MIN(event_time)) AS cohort_date
  FROM `ecommerce_data.fact_events`
  WHERE customer_id IS NOT NULL
  GROUP BY customer_id
),

activity AS (
  SELECT
    f.customer_id,
    f.cohort_date,
    DATE_DIFF(DATE(e.event_time), f.cohort_date, DAY) AS day_number
  FROM `ecommerce_data.fact_events` e
  JOIN first_seen f USING (customer_id)
),

cohort_size AS (
  SELECT
    cohort_date,
    COUNT(DISTINCT customer_id) AS cohort_size
  FROM first_seen
  GROUP BY cohort_date
)

SELECT
  a.cohort_date,
  case when day_number=0 then '0' 
  when day_number between 1 and 7 then 'Week 1'
  when day_number between 8 and 14 then 'Week 2' 
   when day_number between 15 and 21 then 'Week 3'
   when day_number between 22 and 35 then 'Week 4'
   when day_number between 36 and 49 then 'Week 5'
   else '>Week 6'
   end as week_number,
  c.cohort_size,
  COUNT(DISTINCT a.customer_id) AS active_users,
  COUNT(DISTINCT a.customer_id) / c.cohort_size AS retention_rate
FROM activity a
JOIN cohort_size c USING (cohort_date)
GROUP BY 1,2,3 
having week_number<>'0'
ORDER BY 1,2;
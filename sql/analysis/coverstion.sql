WITH funnel AS (
  SELECT
    customer_id,
    MAX(CASE WHEN event_type = 'page_view' THEN 1 ELSE 0 END) AS viewed,
    MAX(CASE WHEN event_type = 'search' THEN 1 ELSE 0 END) AS searched,
    MAX(CASE WHEN event_type = 'add_to_cart' THEN 1 ELSE 0 END) AS added_to_cart
  FROM `my-project-284-493514.ecommerce_data.fact_events`
  where customer_id is not null 
  GROUP BY customer_id
),

purchases AS (
  SELECT customer_id
  FROM `my-project-284-493514.ecommerce_data.dim_payers`
)

SELECT
  COUNT(*) AS total_users,
  SUM(viewed) AS viewers,
  SUM(searched) AS searchers,
  SUM(added_to_cart) AS add_to_cart_users,
  COUNT(p.customer_id) AS total_buyers,
  count( case when added_to_cart=1 then p.customer_id end) as buyers_chart_p,

  -- conversion rates
  round(count(distinct p.customer_id)/ count(*),3) AS payers_rate,
  round(SUM(searched) / SUM(viewed),3) AS view_to_search_rate,
  round(SUM(added_to_cart) / SUM(searched),3) AS search_to_cart_rate, --
  round(COUNT(case when added_to_cart=1 then p.customer_id end) / SUM(added_to_cart),3) AS add_to_cart_to_purchase_rate

FROM funnel f
LEFT JOIN purchases p
ON f.customer_id = p.customer_id;
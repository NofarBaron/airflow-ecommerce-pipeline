SELECT timestamp_TRUNC(order_time, MONTH) as month,
      round(avg(order_amount),0) avg_amount,
      round(sum(order_amount),0) total,
      count(order_id) num_orders
FROM `my-project-284-493514.ecommerce_data.stg_orders`
where status='success'
GROUP BY 1
select category , count(*) orders
FROM `my-project-284-493514.ecommerce_data.stg_products` p
join `my-project-284-493514.ecommerce_data.stg_orders` o
on p.product_id = o.product_id
group by all
having category is not null
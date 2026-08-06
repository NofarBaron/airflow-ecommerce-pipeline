select country, count(*)
from `my-project-284-493514.ecommerce_data.customers` c
join `my-project-284-493514.ecommerce_data.dim_payers` p
 using(customer_id)
group by 1 

select country, count(*)
from `my-project-284-493514.ecommerce_data.customers` c
join `my-project-284-493514.ecommerce_data.stg_orders` o
 using(customer_id)
group by 1 
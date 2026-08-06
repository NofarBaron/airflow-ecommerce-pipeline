SELECT sum(case when lower(status)='refunded' then 1 end) ref,
sum(case when lower(status) in ('success') then 1 end) suc,
sum(case when lower(status) in ('success','refunded') then 1 end) suc_ref,
sum(case when lower(status)='refunded' then 1 end)/sum(case when lower(status) in ('success','refunded') then 1 end) ref_out_all
FROM `my-project-284-493514.ecommerce_data.stg_orders`

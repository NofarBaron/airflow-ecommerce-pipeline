CREATE OR REPLACE TABLE `my-project-284-493514.ecommerce_data.stg_products` AS

WITH cleaned AS (
    SELECT product_id,
        product_name,
       ABS(SAFE_CAST(price AS FLOAT64)) AS price, 
        LOWER(
            TRIM(
                REGEXP_REPLACE(category, r'[^a-zA-Z0-9]', '')
            )
        ) AS cleaned_category,
        ingest_run_id,
        ingested_at
        

FROM `my-project-284-493514.ecommerce_data.product_catalog` 
WHERE product_id IS NOT NULL
AND SAFE_CAST(price AS FLOAT64) IS NOT NULL

)

SELECT
    * except(cleaned_category),
    CASE
        WHEN cleaned_category IN ('electronics','3l3ctronics','ele')
            THEN 'Electronics'

        WHEN cleaned_category IN ('beauty','b3auty','bea')
            THEN 'Beauty'

        WHEN cleaned_category IN ('sports')
            THEN 'Sports'

        WHEN cleaned_category IN ('automotive','automotiv3','aut')
            THEN 'Automotive'

        WHEN cleaned_category IN ('clothing','clo')
            THEN 'Clothing'

        WHEN cleaned_category IN ('home','hom','hom3')
            THEN 'Home'

        WHEN cleaned_category IN ('kitchen','kitch3n','kit')
            THEN 'Kitchen'

        WHEN cleaned_category IN ('toys','toy')
            THEN 'Toys'
        when cleaned_category IS NULL
            THEN cleaned_category
        ELSE 'Unknown'
    END AS category

FROM cleaned;
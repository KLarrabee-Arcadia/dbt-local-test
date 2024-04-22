select
    store_id,
    count(*) as total_customers
from {{ ref('customer_base') }}
group by 1

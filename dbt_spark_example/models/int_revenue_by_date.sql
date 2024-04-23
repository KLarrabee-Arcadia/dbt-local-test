select
    date(payment_date) as payment_date,
    sum(amount) as amount
from {{ ref('stg_payment') }}
group by 1

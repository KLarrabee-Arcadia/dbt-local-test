select *
from {{ source('public', 'payment') }}

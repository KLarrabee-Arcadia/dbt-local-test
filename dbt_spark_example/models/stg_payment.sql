select *
from {{ source('hudi_sources', 'payment') }}

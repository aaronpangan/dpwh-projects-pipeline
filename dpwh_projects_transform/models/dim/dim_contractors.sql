with parsed as (
    select * from {{ ref('int_contractors_parsed') }}
)

select
    contractor_pk,
    contractor_name,
    contractor_code
from parsed
group by 1, 2, 3
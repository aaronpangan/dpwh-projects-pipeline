with parsed as (
    select * from {{ ref('int_contractors_parsed') }}
)

select
    contract_id,
    contractor_pk,
    position
from parsed
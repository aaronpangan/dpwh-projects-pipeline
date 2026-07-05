with parsed as (
    select * from {{ ref('int_contractors_parsed') }}
)

-- One row per contractor_pk. contractor_pk is hashed from contractor_name, so a
-- contractor whose name appears under several codes must still collapse to a
-- single row. max() keeps one representative code and prefers a real code over a
-- null/blank.
select
    contractor_pk,
    contractor_name,
    max(contractor_code) as contractor_code
from parsed
group by contractor_pk, contractor_name
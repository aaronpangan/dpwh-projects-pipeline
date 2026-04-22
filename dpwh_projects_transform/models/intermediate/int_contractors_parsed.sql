with source as (
    select 
        contract_id,
        contractor_raw
    from {{ ref('stg_dpwh_projects') }}
),

flattened as (
    select
        contract_id,
        contractor_raw,
        trim(f.value::string) as contractor_segment,
        f.index + 1 as position
    from source,
    lateral flatten(input => split(contractor_raw, ' / ')) f
),

parsed as (
    select
        contract_id,
        contractor_raw,
        contractor_segment,
        position,
        -- Extract name: everything before the last '('
        upper(trim(regexp_replace(contractor_segment, '\\s*\\([^)]*\\)$', ''))) as contractor_name,
        -- Extract code: everything inside the parentheses
        regexp_substr(contractor_segment, '\\(([^)]+)\\)', 1, 1, 'e') as contractor_code
    from flattened
)

select
    contract_id,
    {{ dbt_utils.generate_surrogate_key(['contractor_name']) }} as contractor_pk,
    position,
    contractor_segment,
    contractor_name,
    contractor_code,
    contractor_raw
from parsed
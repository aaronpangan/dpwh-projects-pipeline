-- models/marts/brg_project_components.sql
with exploded as (
    select
        p.contract_id,
        trim(c.value::string) as raw_category
    from {{ ref('stg_dpwh_projects') }} p,
    lateral flatten(input => split(
        coalesce(nullif(component_categories, 'Null'), 'Uncategorized'), ','
    )) c
)

select
    e.contract_id,
    -- We join to the dim to make sure we only use "Official" categories
    d.component_category
from exploded e
left join {{ ref('dim_categories') }} d 
    on e.raw_category = d.component_category
    -- If it's Consultancy or something weird, it won't match, so we coalesce to Uncategorized
    or (d.component_category = 'Uncategorized' and (e.raw_category = 'Consultancy' or e.raw_category not in (
        'Bridges', 'Buildings and Facilities', 'Flood Control and Drainage', 
        'Roads', 'Septage and Sewerage Plants', 'Water Provision and Storage'
    )))
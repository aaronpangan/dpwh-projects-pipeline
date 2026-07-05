{{ config(materialized='table') }}

-- One row per project (contract_id) — joins fct_projects to location detail and
-- collapses the many-to-many contractor and category relationships into
-- delimited strings so project grain is preserved.

with projects as (
    select * from {{ ref('fct_projects') }}
),

locations as (
    select * from {{ ref('dim_locations') }}
),

categories_per_project as (
    select
        contract_id,
        listagg(distinct component_category, ', ')
            within group (order by component_category) as component_categories,
        count(distinct component_category)              as category_count
    from {{ ref('brg_project_categories') }}
    group by contract_id
),

contractors_per_project as (
    select
        b.contract_id,
        listagg(distinct c.contractor_name, ' / ')
            within group (order by c.contractor_name) as contractor_names,
        listagg(distinct c.contractor_code, ', ')
            within group (order by c.contractor_code) as contractor_codes,
        count(distinct b.contractor_pk)                as contractor_count,
        max(case when b.position = 1 then c.contractor_name end) as lead_contractor_name
    from {{ ref('brg_contractors') }} b
    join {{ ref('dim_contractors') }} c
        on b.contractor_pk = c.contractor_pk
    group by b.contract_id
)

select
    -- keys
    p.contract_id,
    p.location_key,

    -- location
    l.island_group,
    l.region,
    l.province_name,
    l.executing_office,
    l.is_upmo,
    l.is_regional_level,

    -- descriptive
    p.project_description,
    p.project_category,
    p.program_name,
    p.source_of_funds,
    p.infra_year,

    -- categories (collapsed from bridge)
    cat.component_categories,
    cat.category_count,

    -- contractors (collapsed from bridge)
    con.contractor_names,
    con.contractor_codes,
    con.contractor_count,
    con.lead_contractor_name,
    case when con.contractor_count > 1 then true else false end as is_joint_venture,

    -- status and measures
    p.project_status,
    p.budget_amount,
    p.budget_tier,
    p.progress_pct,
    p.duration_days,

    -- dates
    p.start_date,
    p.completion_date,

    -- flags
    p.is_delayed,
    p.is_ghost_project,
    p.is_completed,

    -- url + metadata
    p.project_url,
    p.last_updated_at

from projects p
left join locations l
    on p.location_key = l.location_key
left join categories_per_project cat
    on p.contract_id = cat.contract_id
left join contractors_per_project con
    on p.contract_id = con.contract_id

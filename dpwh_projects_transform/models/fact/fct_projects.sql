{{ config(
    materialized='table'
) }}

with staging as (
    select * from {{ ref('stg_dpwh_projects') }}
),

locations as (
    select * from {{ ref('dim_locations') }}
),

final as (
    select
        -- primary key
        s.contract_id,

        -- foreign keys
        l.location_key,

        -- degenerate dimensions
        s.project_description,
        s.project_category,
        s.program_name,
        s.source_of_funds,
        s.project_status,
        s.infra_year,

        -- measures
        s.budget_amount,
        s.progress_pct,
        s.duration_days,

        -- dates
        s.start_date,
        s.completion_date,

        -- flags
        s.is_delayed,
        s.is_ghost_project,
        s.is_completed,

        -- classifications
        s.budget_tier,

        -- project url
        'https://transparency.dpwh.gov.ph/?project=' || s.contract_id as project_url,

        -- metadata
        s.last_updated_at

    from staging s
    left join locations l
        on md5(cast(coalesce(s.region, '') || coalesce(s.province, '') as string))
         = l.location_key
)

select * from final
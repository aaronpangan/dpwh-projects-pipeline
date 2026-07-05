{{ config(materialized='table') }}

select
    l.island_group,
    l.region,
    l.province_name,
    count(f.contract_id)                                        as total_projects,
    sum(f.budget_amount)                                        as total_budget,
    avg(f.budget_amount)                                        as avg_budget,
    count_if(f.is_completed)                                    as completed_projects,
    count_if(f.is_delayed)                                      as delayed_projects,
    count_if(f.is_ghost_project)                                as ghost_projects,
    round(count_if(f.is_completed) * 100.0 / nullif(count(*), 0), 2) as completion_rate_pct,
    round(count_if(f.is_delayed) * 100.0 / nullif(count(*), 0), 2)   as delay_rate_pct,
    round(count_if(f.is_ghost_project) * 100.0 / nullif(count(*), 0), 2) as ghost_rate_pct
from {{ ref('fct_projects') }} f
join {{ ref('dim_locations') }} l
    on f.location_key = l.location_key
group by
    l.island_group,
    l.region,
    l.province_name
{{ config(materialized='table') }}

-- One row per contractor. Aggregates project counts, budget, and performance
-- rates across every contract a contractor was party to.
--
-- Attribution: joint ventures credit the FULL project budget to every
-- contractor involved. A 10M project shared by two contractors contributes
-- 10M to each contractor's total_budget. This means summing total_budget
-- across this mart will exceed the true portfolio total — that is expected
-- and is the standard analytical choice for contractor-performance views.

with contractor_projects as (
    select
        b.contractor_pk,
        f.contract_id,
        f.budget_amount,
        f.is_completed,
        f.is_delayed,
        f.is_ghost_project,
        b.position
    from {{ ref('brg_contractors') }} b
    join {{ ref('fct_projects') }} f
        on b.contract_id = f.contract_id
),

aggregated as (
    select
        contractor_pk,
        count(distinct contract_id)                                              as total_projects,
        count_if(position = 1)                                                   as lead_contractor_projects,
        count_if(position > 1)                                                   as joint_venture_projects,
        sum(budget_amount)                                                       as total_budget,
        avg(budget_amount)                                                       as avg_budget,
        count_if(is_completed)                                                   as completed_projects,
        count_if(is_delayed)                                                     as delayed_projects,
        count_if(is_ghost_project)                                               as ghost_projects,
        round(count_if(is_completed)     * 100.0 / nullif(count(distinct contract_id), 0), 2)       as completion_rate_pct,
        round(count_if(is_delayed)       * 100.0 / nullif(count(distinct contract_id), 0), 2)       as delay_rate_pct,
        round(count_if(is_ghost_project) * 100.0 / nullif(count(distinct contract_id), 0), 2)       as ghost_rate_pct
    from contractor_projects
    group by contractor_pk
)

select
    c.contractor_pk,
    c.contractor_code,
    c.contractor_name,
    a.total_projects,
    a.lead_contractor_projects,
    a.joint_venture_projects,
    a.total_budget,
    a.avg_budget,
    a.completed_projects,
    a.delayed_projects,
    a.ghost_projects,
    a.completion_rate_pct,
    a.delay_rate_pct,
    a.ghost_rate_pct
from aggregated a
join {{ ref('dim_contractors') }} c
    on a.contractor_pk = c.contractor_pk

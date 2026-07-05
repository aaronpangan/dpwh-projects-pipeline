{{ config(materialized='table') }}

-- One row per category. Aggregates project counts, budget, and performance
-- metrics by infrastructure category via the brg_project_categories bridge.
--
-- Attribution: multi-category projects credit the FULL budget to every
-- category they touch. A 10M project tagged [Bridges, Roads] contributes
-- 10M to Bridges and 10M to Roads. Summing total_budget across this mart
-- will therefore exceed the true portfolio total — this is the standard
-- analytical choice for category breakdowns and matches the DPWH
-- transparency portal's own charts.

with categorized as (
    select
        d.component_category,
        d.category_sort_order,
        d.category_description,
        f.contract_id,
        f.budget_amount,
        f.is_completed,
        f.is_delayed,
        f.is_ghost_project
    from {{ ref('fct_projects') }} f
    join {{ ref('brg_project_categories') }} b
        on f.contract_id = b.contract_id
    join {{ ref('dim_categories') }} d
        on b.component_category = d.component_category
)

select
    component_category,
    category_sort_order,
    category_description,
    count(distinct contract_id)                                              as total_projects,
    sum(budget_amount)                                                       as total_budget,
    avg(budget_amount)                                                       as avg_budget,
    count_if(is_completed)                                                   as completed_projects,
    count_if(is_delayed)                                                     as delayed_projects,
    count_if(is_ghost_project)                                               as ghost_projects,
    round(count_if(is_completed)     * 100.0 / nullif(count(distinct contract_id), 0), 2)       as completion_rate_pct,
    round(count_if(is_delayed)       * 100.0 / nullif(count(distinct contract_id), 0), 2)       as delay_rate_pct,
    round(count_if(is_ghost_project) * 100.0 / nullif(count(distinct contract_id), 0), 2)       as ghost_rate_pct
from categorized
group by
    component_category,
    category_sort_order,
    category_description
order by category_sort_order

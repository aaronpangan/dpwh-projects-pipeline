with source as (
    select * from {{ source('raw', 'RAW_DPWH_PROJECTS') }}
),

staged as (
    select
        -- keys
        contractid                              as contract_id,

        -- descriptive
        description                             as project_description,
        category                                as project_category,
        componentcategories                     as component_categories,
        programname                             as program_name,
        sourceoffunds                           as source_of_funds,
        infrayear::integer                      as infra_year,

        -- status and progress
        status                                  as project_status,
        progress::float                         as progress_pct,
        budget::float                           as budget_amount,

        -- contractor
        contractor                              as contractor_raw,

        -- location
        province,
        region,
        latitude::float                         as latitude,
        longitude::float                        as longitude,

        -- dates
        try_to_date(startdate)                  as start_date,
        try_to_date(completiondate)             as completion_date,

    
        -- metadata
        last_updated_at,

        -- derived fields
        case
            when try_to_date(completiondate) is not null
                and try_to_date(startdate) is not null
            then datediff('day', try_to_date(startdate), try_to_date(completiondate))
            else null
        end                                     as duration_days,

        case
            when status = 'Completed' and progress < 100
            then true
            when status != 'Completed' and try_to_date(completiondate) < current_date()
            then true
            else false
        end                                     as is_delayed,

        case
            when progress = 0
                and budget > 0
                and status not in ('For Procurement', 'Not Started')
            then true
            else false
        end                                     as is_ghost_project,

        case
            when budget < 1000000           then 'Small'
            when budget < 10000000          then 'Medium'
            when budget < 100000000         then 'Large'
            else                                 'Major'
        end                                     as budget_tier,

        case
            when status = 'Completed'       then true
            else                                 false
        end                                     as is_completed

    from source
)

select * from staged

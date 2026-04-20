{{ config(
    materialized='table'
) }}

with unique_source_locations as (
    select distinct 
        region, 
        province as raw_province 
    from {{ ref('stg_dpwh_projects') }}
),

transformed_locations as (
    select
        region,
        raw_province,
        
        case 
            when raw_province ilike any ('%cluster%', '%bureau%') 
                then 'UPMO / Central Office'
            
            when raw_province = region 
                then 'Regional Office / Multi-Province'
            
            when raw_province ilike '%deo%' then 
                trim(
                    left(
                        raw_province, 
                        coalesce(
                            nullif(regexp_instr(raw_province, ' ([0-9]|DEO|Sub)'), 0) - 1, 
                            len(raw_province)
                        )
                    )
                )
            
            else raw_province 
        end as province_name,

        case 
            when region in (
                'National Capital Region', 'Region I', 'Region II', 'Region III', 
                'Region IV-A', 'Region IV-B', 'Region V', 'Cordillera Administrative Region'
            ) then 'Luzon'
            when region in (
                'Region VI', 'Region VII', 'Region VIII', 'Negros Island Region'
            ) then 'Visayas'
            when region in (
                'Region IX', 'Region X', 'Region XI', 'Region XII', 'Region XIII'
            ) then 'Mindanao'
            when region = 'Central Office' then 'National / Central Office'
            else 'Unknown'
        end as island_group

    from unique_source_locations
)

select
    -- This key is what you will use to JOIN to the Fact table later
    md5(cast(coalesce(region, '') || coalesce(raw_province, '') as string)) as location_key,
    
    island_group,
    region,
    initcap(province_name) as province_name,
    raw_province as executing_office,
    
    case when province_name = 'UPMO / Central Office' then true else false end as is_upmo,
    case when province_name = 'Regional Office / Multi-Province' then true else false end as is_regional_level

from transformed_locations
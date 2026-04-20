-- models/marts/dim_component_categories.sql
with categories (component_category, category_sort_order, category_description) as (
    select * from (values
        ('Bridges', 1, 'Bridge infrastructure projects.'),
        ('Buildings and Facilities', 2, 'Vertical infrastructure and public facility projects.'),
        ('Flood Control and Drainage', 3, 'Water management and disaster mitigation infrastructure projects.'),
        ('Roads', 4, 'Road network construction and rehabilitation projects.'),
        ('Septage and Sewerage Plants', 5, 'Sanitation and wastewater management projects.'),
        ('Water Provision and Storage', 6, 'Water supply and storage infrastructure projects.'),
        ('Uncategorized', 7, 'Contracts with missing, null, or unclassified component categories.')
    )
)

select * from categories
order by category_sort_order
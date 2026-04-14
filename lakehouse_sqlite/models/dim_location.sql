with source as (
    select distinct
        pulocationid as location_id
    from main.raw_taxi_trips
    union
    select distinct
        dolocationid as location_id
    from main.raw_taxi_trips
)
select
    location_id,
    case
        when location_id between 1 and 100 then 'Manhattan'
        when location_id between 101 and 200 then 'Brooklyn'
        when location_id between 201 and 265 then 'Queens'
        else 'Other'
    end as borough
from source
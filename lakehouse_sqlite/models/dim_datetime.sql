with source as (
    select distinct
        tpep_pickup_datetime,
        strftime('%Y', tpep_pickup_datetime) as year,
        strftime('%m', tpep_pickup_datetime) as month,
        strftime('%d', tpep_pickup_datetime) as day,
        strftime('%H', tpep_pickup_datetime) as hour,
        case cast(strftime('%w', tpep_pickup_datetime) as integer)
            when 0 then 'Sunday'
            when 1 then 'Monday'
            when 2 then 'Tuesday'
            when 3 then 'Wednesday'
            when 4 then 'Thursday'
            when 5 then 'Friday'
            when 6 then 'Saturday'
        end as day_of_week
    from main.raw_taxi_trips
)
select
    row_number() over () as datetime_id,
    tpep_pickup_datetime,
    year,
    month,
    day,
    hour,
    day_of_week
from source
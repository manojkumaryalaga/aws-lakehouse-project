with source as (
    select
        vendorid,
        tpep_pickup_datetime,
        tpep_dropoff_datetime,
        passenger_count,
        trip_distance,
        pulocationid,
        dolocationid,
        payment_type,
        fare_amount,
        tip_amount,
        tolls_amount,
        total_amount
    from main.raw_taxi_trips
)
select
    row_number() over () as trip_id,
    vendorid,
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    passenger_count,
    trip_distance,
    pulocationid,
    dolocationid,
    payment_type,
    fare_amount,
    tip_amount,
    tolls_amount,
    total_amount
from source
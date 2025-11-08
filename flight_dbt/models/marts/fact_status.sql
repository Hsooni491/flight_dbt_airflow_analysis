-- models/marts/fact_status.sql
WITH flights_info AS (
	SELECT
    flight_date,
    flight_status,
    COUNT(*) AS flights_count
FROM {{ ref('stg_flights') }}
GROUP BY flight_date, flight_status
)

SELECT * FROM flights_info

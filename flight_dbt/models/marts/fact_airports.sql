WITH airport_info AS (
	SELECT
    dep_airport AS airport,
    COUNT(*) AS total_departures,
    SUM(CASE WHEN flight_status = 'delayed' THEN 1 ELSE 0 END) AS delayed_departures,
    ROUND(
        (SUM(CASE WHEN flight_status = 'delayed' THEN 1 ELSE 0 END)::decimal 
         / COUNT(*)) * 100, 2
    ) AS delay_percentage
FROM {{ ref('stg_flights') }}
GROUP BY dep_airport
)


SELECT * FROM airport_info

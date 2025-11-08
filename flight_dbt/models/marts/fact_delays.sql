WITH airport_delays AS (
    SELECT
        airline,
        COUNT(*) AS total_flights,
        SUM(CASE WHEN flight_status = 'delayed' THEN 1 ELSE 0 END) AS delayed_flights,
        ROUND(AVG(dep_delay_minutes), 2) AS avg_dep_delay,
        ROUND(AVG(arr_delay_minutes), 2) AS avg_arr_delay,
        ROUND(
            AVG(COALESCE(dep_delay_minutes, 0)) + AVG(COALESCE(arr_delay_minutes, 0)), 2
        ) AS avg_total_delay
    FROM {{ ref('stg_flights') }}
    GROUP BY airline
)

SELECT * FROM airport_delays
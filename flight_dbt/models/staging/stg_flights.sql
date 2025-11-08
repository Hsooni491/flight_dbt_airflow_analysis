SELECT 
	flight_id,
	flight_date,
	airline_name AS airline,
	flight_number,
	dep_airport,
	dep_delay_time::INTEGER AS dep_delay_minutes,
	dep_time,
	arr_airport,
	arr_time,
	flight_status,
	arr_delay_minutes::INTEGER,
	(dep_delay_time + COALESCE(arr_delay_minutes, 0)) AS total_delay_minutes
FROM {{ source('public', 'raw_flights') }}
WHERE (dep_delay_time IS NOT NULL) AND (arr_delay_minutes < 15 OR arr_delay_minutes IS NULL)
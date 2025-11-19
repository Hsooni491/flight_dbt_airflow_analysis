SELECT 
	flight_id,
	flight_date,
	airline_name AS airline,
	flight_number,
	dep_airport,
	CAST(dep_delay_time AS INTEGER) AS dep_delay_minutes,
	dep_time,
	arr_airport,
	arr_time,
	flight_status,
	CAST(arr_delay_minutes AS INTEGER),
	(CAST(dep_delay_time AS INTEGER) + COALESCE(CAST(arr_delay_minutes AS INTEGER), 0)) AS total_delay_minutes
FROM {{ source('public', 'raw_flights') }}
WHERE (CAST(dep_delay_time AS INTEGER) IS NOT NULL) AND (CAST(arr_delay_minutes AS INTEGER) < 15 OR arr_delay_minutes IS NULL)
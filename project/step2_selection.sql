select distinct flight_number, airline_name, departure_date_time from Flight
	where departure_date_time > NOW();
select distinct flight_number, airline_name, departure_date_time from Flight
	where status = "delay";
select distinct name from Customer join Buy;
select distinct airplane_id from Airplane
	where airline_name="China Eastern";

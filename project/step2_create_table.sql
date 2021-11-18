create table Airport(
code 		int, 
name 		varchar(20) not null, 
city 		varchar(20) not null,
primary key(code)
);

create table Airline(
airline_name 	varchar(20), 
primary key(airline_name)
);

create table Customer(
email 		varchar(20),
name	 	varchar(300) not null,
password 	varchar(300) not null,
building_number 	varchar(20),
street 		varchar(20),
city 		varchar(20),
state 		varchar(20), 
phone_number 	varchar(10) not null,
passport_number 	char(9) not null,
passport_expiration date not null,
passport_country 	varchar(20) not null,
date_of_birth 	date not null,
primary key(email),
check(email like ('%@%'))
);

-- relational
create table Airplane(
airline_name 	varchar(20),
airplane_id 	varchar(20),
num_seats 	int not null,
primary key(airline_name, airplane_id),
foreign key(airline_name) references Airline
	on delete cascade
	on update cascade
);

create table Staff(
username 	varchar(300), 
password 	varchar(300) not null,
first_name 	varchar(20) not null,
last_name 	varchar(20) not null,
date_of_birth 	date not null,
airline_name 	varchar(20),
primary key(username),
foreign key(airline_name) references Airline
	on delete cascade
	on update cascade
);

create table staff_phone(
username 	varchar(300),
phone_number	varchar(10),
primary key(username, phone_number),
foreign key(username) references Staff
	on delete cascade
	on update cascade
);

create table Flight(
flight_number 		varchar(20), 
departure_date_time 	timestamp,
airline_name 		varchar(20),
arrival_date_time 		timestamp,
base_price 		float not null,
status 			varchar(20) not null,
airplane_id 		varchar(20),
depart_airport_code 	int,
arrive_airport_code 	int,
primary key(flight_number, departure_date_time, airline_name),
foreign key(depart_airport_code, arrive_airport_code) references Airport
	on delete cascade
	on update cascade,
foreign key(airline_name) references Airline
	on delete cascade
	on update cascade,
foreign key(airplane_id) references Airplane
	on delete cascade
	on update cascade,
check(status in("delay", "ontime"))
);

create table Ticket(
ticket_id 			varchar(20),
flight_number 		varchar(20), 
departure_date_time 	timestamp,
airline_name 		varchar(20),
primary key(ticket_id),
foreign key(flight_number, departure_date_time, airline_name) references Flight
	on delete cascade
	on update cascade
);

create table Rate(
email 			varchar(20),
airline_name 		varchar(20),
departure_date_time 	timestamp,
flight_number 		varchar(20),
rating 			numeric(2,1),
comment 		varchar(300),
primary key(email, airline_name, departure_date_time, flight_number),
foreign key(email) references Customer
	on delete cascade
	on update cascade,
foreign key(airline_name, departure_date_time, flight_number) references Flight
	on delete cascade
	on update cascade,
check(rating in(0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0))
);


create table Buy(
ticket_id 		varchar(20),
email 		varchar(20),
purcahse_date_time timestamp not null,
name_on_card 	varchar(40) not null,
card_num              varchar(16) not null,
card_type 	varchar(20) not null,
expiration_date 	date not null,
primary key(ticket_id),
foreign key(ticket_id) references Ticket
	on delete cascade
	on update cascade,
foreign key(email) references Customer
	on delete cascade
	on update cascade,
check(card_type in ('credit', 'debit'))
);
insert into airline values("China Eastern");
insert into airport values(1,"JFK", "NYC");
insert into airport values(2,"PVG", "Shanghai");
insert into customer values("yw4177@nyu.edu", "Yishi Wang", "12345678", "2", "100willoughby street", "Brooklyn","NY", "9178922307","EB3312345", "2024-12-1", "China", "2001-3-1");
insert into customer values("yw4167@nyu.edu", "Tomus Liu", "12345678", "15", "100willoughby street", "Brooklyn","NY", "9178922308","EB5512345", "2024-12-1", "China", "2000-3-1");
insert into customer values("yw4157@nyu.edu", "James", "12345678", "20", "100willoughby street", "Brooklyn","NY", "9178922309","EB4512345", "2024-12-1", "China", "1999-3-1");
insert into Airplane values("China Eastern", "B1", 500);
insert into Airplane values("China Eastern", "B2", 400);
insert into Airplane values("China Eastern", "B3", 400);
insert into Staff values("Tom", "123456789", "Lambert", "Li", "1980-4-5", "China Eastern");
insert into staff_phone values("Tom", "9192897998");
insert into Flight values("AB123", "2021-11-9 12:00:00", "China Eastern", "2021-11-20 18:00:00", 300, "delay", "B1", 1,2);
insert into Flight values("AC123", "2021-11-9 19:00:00", "China Eastern", "2021-11-19 14:00:00", 300, "ontime", "B1", 2,1);
insert into Ticket values("A0001", "AB123", "2021-11-9 12:00:00", "China Eastern");
insert into Ticket values("A0002", "AB123", "2021-11-9 12:00:00", "China Eastern");
insert into Ticket values("A0003", "AB123", "2021-11-9 12:00:00", "China Eastern");
insert into Ticket values("A0004", "AB123", "2021-11-9 12:00:00", "China Eastern");
insert into Ticket values("A0005", "AB123", "2021-11-9 12:00:00", "China Eastern");
insert into Ticket values("A0006", "AB123", "2021-11-9 12:00:00", "China Eastern");
insert into Buy values("A0001", "yw4177@nyu.edu", "2021-11-7 12:08:12", "Yishi Wang", "1234567890123456","credit", "2024-12-01");
insert into Buy values("A0002", "yw4167@nyu.edu", "2021-11-7 12:05:12", "allen", "1234567890723456", "debit", "2024-12-01");
# Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import time
import datetime

# Initialize the app from Flask
app = Flask(__name__)

# Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password="",
                       db='project',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


# Define a route to hello function
@app.route('/')
def hello():
    return render_template('index.html')


# Define route for login
@app.route('/login')
def login():
    return render_template('login.html')


# Define route for register
@app.route('/register_choose')
def register():
    return render_template('register_choose.html')


@app.route('/staff_register')
def register_staff():
    # TODO:
    return render_template("register_staff.html")


@app.route('/customer_register')
def register_customer():
    # TODO:
    return render_template("register_customer.html")


@app.route('/flight_search', methods=['GET', 'POST'])
def flight_search():
    trip_type = request.form['trip_type']
    source_city = request.form['source_city']
    source_airport = request.form['source_airport']
    des_city = request.form['des_city']
    des_airport = request.form['des_airport']
    date = request.form["departure_date"]
    return_date = request.form["return_date"]
    cursor = conn.cursor()
    if trip_type == "round":
        query = "SELECT e.flight_number, e.departure_date_time as departure_date, e.airline_name, " \
                "f.flight_number as return_flight_number, date(f.departure_date_time) as return_date, " \
                "f.airline_name as return_airline_name from(SELECT b.flight_number, b.departure_date_time, " \
                "b.airline_name, arrival_date_time FROM Airport as a join Flight as b on b.depart_airport_code=a.code " \
                "join Airport as c on b.arrive_airport_code=c.code WHERE a.city= %s and a.name=%s and c.city=%s " \
                "and c.name=%s and date(b.departure_date_time) = %s)e inner join(SELECT b.flight_number, " \
                "b.departure_date_time, b.airline_name FROM Airport as a join Flight as b on b.depart_airport_code=a.code " \
                "join Airport as c on b.arrive_airport_code=c.code WHERE a.city= %s and a.name=%s and c.city=%s " \
                "and c.name=%s and date(b.departure_date_time) = %s)f on e.arrival_date_time < f.departure_date_time"
        cursor.execute(query, (
            source_city, source_airport, des_city, des_airport, date, des_city, des_airport, source_city,
            source_airport,
            return_date))
    else:
        query = 'SELECT b.flight_number, b.departure_date_time, b.airline_name, ""as return_flight_number, "" as return_date, ""as return_airline_name ' \
                'FROM Airport as a join (select flight_number, departure_date_time, ' \
                'airline_name, depart_airport_code, arrive_airport_code from Flight)as b ' \
                'on b.depart_airport_code=a.code join Airport as c on b.arrive_airport_code=c.code WHERE a.city= %s ' \
                'and a.name=%s and c.city=%s and c.name=%s and date(b.departure_date_time) = %s'
        cursor.execute(query, (source_city, source_airport, des_city, des_airport, date))
    data = cursor.fetchall()
    cursor.close()
    ##error = "Error with the input"
    if (not data):
        error = "No flight founded, please check your flight information"
        return render_template("index.html", error1=error)
        ##error = "Error with the input"
    return render_template("index.html", posts1=data)


@app.route('/flight_search_home', methods=['GET', 'POST'])
def flight_search_home():
    trip_type = request.form['trip_type']
    source_city = request.form['source_city']
    source_airport = request.form['source_airport']
    des_city = request.form['des_city']
    des_airport = request.form['des_airport']
    date = request.form["departure_date"]
    return_date = request.form["return_date"]
    cursor = conn.cursor()
    if trip_type == "round":
        query = "SELECT e.flight_number, e.departure_date_time as departure_date, e.airline_name, " \
                "f.flight_number as return_flight_number, date(f.departure_date_time) as return_date, " \
                "f.airline_name as return_airline_name from(SELECT b.flight_number, b.departure_date_time, " \
                "b.airline_name, arrival_date_time FROM Airport as a join Flight as b on b.depart_airport_code=a.code " \
                "join Airport as c on b.arrive_airport_code=c.code WHERE a.city= %s and a.name=%s and c.city=%s " \
                "and c.name=%s and date(b.departure_date_time) = %s)e inner join(SELECT b.flight_number, " \
                "b.departure_date_time, b.airline_name FROM Airport as a join Flight as b on b.depart_airport_code=a.code " \
                "join Airport as c on b.arrive_airport_code=c.code WHERE a.city= %s and a.name=%s and c.city=%s " \
                "and c.name=%s and date(b.departure_date_time) = %s)f on e.arrival_date_time < f.departure_date_time"
        cursor.execute(query, (
            source_city, source_airport, des_city, des_airport, date, des_city, des_airport, source_city,
            source_airport,
            return_date))
    else:
        query = 'SELECT b.flight_number, b.departure_date_time, b.airline_name, ""as return_flight_number, "" as return_date, ""as return_airline_name ' \
                'FROM Airport as a join (select flight_number, departure_date_time, ' \
                'airline_name, depart_airport_code, arrive_airport_code from Flight)as b ' \
                'on b.depart_airport_code=a.code join Airport as c on b.arrive_airport_code=c.code WHERE a.city= %s ' \
                'and a.name=%s and c.city=%s and c.name=%s and date(b.departure_date_time) = %s'
        cursor.execute(query, (source_city, source_airport, des_city, des_airport, date))
    data = cursor.fetchall()
    cursor.close()
    ##error = "Error with the input"
    if (not data):
        error = "No flight founded, please check your flight information"
        return render_template("customer_home.html", error1=error)
    return render_template("customer_home.html", posts1=data)


@app.route('/See_status', methods=['GET', 'POST'])
def See_status():
    # TODO: check
    airline_name = request.form['airline_name']
    flight_number = request.form['flight_number']
    dep_date = request.form['departure_date']
    dep_date = dep_date.replace("T", " ") + ":00"
    cursor = conn.cursor()
    query = 'SELECT a.status FROM ' \
            '(select status, flight_number, departure_date_time, ' \
            'airline_name from flight)as a ' \
            'WHERE a.flight_number = %s and a.departure_date_time=%s and a.airline_name=%s '
    cursor.execute(query, (flight_number, dep_date, airline_name))
    data = cursor.fetchone()
    cursor.close()
    if (not data):
        error = "No flight founded, please check your flight information"
        return render_template("index.html", error2=error)
    ##error = "Error with the input"
    return render_template("index.html", status=data["status"])


@app.route('/customer_home/<int:if_initial>', methods=['GET', 'POST'])
def customer_home(if_initial):
    username = session['username']
    cursor = conn.cursor()
    if if_initial == 0:
        flight_type = request.form['flight_type']
    else:
        flight_type = "Future"
    if flight_type == "All":
        query = "SELECT flight_number,departure_date_time as dep,airline_name, buy.ticket_id " \
                "FROM customer natural join buy natural join ticket " \
                "WHERE email = %s ORDER BY departure_date_time DESC"
    elif flight_type == "Past":
        query = "SELECT flight_number,departure_date_time as dep,airline_name, buy.ticket_id " \
                "FROM customer natural join buy natural join ticket " \
                "WHERE email = %s and departure_date_time < now() ORDER BY departure_date_time DESC"
    else:
        query = "SELECT flight_number,departure_date_time as dep,airline_name, buy.ticket_id " \
                "FROM customer natural join buy natural join ticket " \
                "WHERE email = %s and departure_date_time >= now() ORDER BY departure_date_time DESC"
    cursor.execute(query, (username))
    data1 = cursor.fetchall()
    query = "SELECT b.flight_number,b.departure_date_time, b.airline_name FROM buy as a natural " \
            "join ticket as b natural join rate as c WHERE a.email=%s and b.departure_date_time <= now() and c.rating is null"
    cursor.execute(query, (username))
    data2 = cursor.fetchall()
    query = "SELECT sum(case when b.price is not null then b.price else 0 end) as total_spend " \
            "from (select distinct year(date) as year, month(date) as month " \
            "from calendar where date between DATE_ADD(now(), INTERVAL-12 MONTH) and now() group by month)as a " \
            "left join (select * from buy where email = %s and date(purchase_date_time) between DATE_ADD(now(), INTERVAL-12 MONTH) and now())as b " \
            "on a.year = year(b.purchase_date_time) and a.month = month(b.purchase_date_time)"
    cursor.execute(query, (username))
    past_year_spend = cursor.fetchone()["total_spend"]
    query = "SELECT sum(case when b.price is not null then b.price else 0 end) as total_spend, " \
            "a.year, a.month from (select distinct year(date) as year, month(date) as month " \
            "from calendar where date between DATE_ADD(now(), INTERVAL-6 MONTH) and now() group by month)as a " \
            "left join (select * from buy where email = %s and date(purchase_date_time) between DATE_ADD(now(),INTERVAL-6 MONTH)and now())as b " \
            "on a.year = year(b.purchase_date_time) and a.month = month(b.purchase_date_time) group by year,month Order by year, month desc"
    cursor.execute(query, (username))
    last_6_month_spend = cursor.fetchall()
    cursor.close()
    return render_template('customer_home.html', username=username, future_flight=data1, flight_type=flight_type,
                           not_commented_flights=data2, last_6_month_spend=last_6_month_spend,
                           past_year_spend=past_year_spend)


# TODO
@app.route('/buy_ticket', methods=['GET', 'POST'])
def buy_ticket():
    username = session['username']
    card_type = request.form["card"]
    if (not card_type):
        error = "Please check the box for card type"
        return render_template('customer_home.html', username=username, error2=error)
    flight_number = request.form["flight_number"]
    airline_name = request.form["airline_name"]
    dep_date = request.form["departure_date"]
    name_on_card = request.form["name_on_card"]
    card_num = request.form["card_num"]
    expir_date = request.form["expiration_date"]
    cursor = conn.cursor()
    dep_date = dep_date.replace("T", " ") + ":00"
    query = "SELECT flight_number,departure_date_time,airline_name FROM flight " \
            "WHERE departure_date_time>= now() and flight_number= %s and airline_name = %s and departure_date_time = %s"
    cursor.execute(query, (flight_number, airline_name, dep_date))
    data = cursor.fetchall()
    if (not data):
        error = "Please check the flight information"
        return render_template('customer_home.html', username=username, error2=error)
    query = "SELECT ticket_id FROM ticket WHERE flight_number=%s and departure_date_time=%s " \
            "and airline_name=%s and ticket_id not in (SELECT ticket_id FROM buy) LIMIT 1"
    cursor.execute(query, (flight_number, dep_date, airline_name))
    ticket_id = cursor.fetchone()["ticket_id"]
    if not ticket_id:
        return render_template('customer_home.html', username=username, fault="the flight is full")
    else:
        query = "SELECT count(distinct ticket_id) as remain, num_seats FROM ticket natural join airplane natural join flight " \
                "WHERE flight_number=%s and departure_date_time=%s and airline_name=%s and ticket_id not in (SELECT ticket_id FROM buy) group by num_seats"
        cursor.execute(query, (flight_number, dep_date, airline_name))
        remain = int(cursor.fetchone()["remain"])
        query = "SELECT count(distinct ticket_id) as remain, num_seats FROM ticket natural join airplane natural join flight " \
                "WHERE flight_number=%s and departure_date_time=%s and airline_name=%s and ticket_id not in (SELECT ticket_id FROM buy) group by num_seats"
        cursor.execute(query, (flight_number, dep_date, airline_name))
        num_seats = float(cursor.fetchone()["num_seats"])
        query = "SELECT distinct base_price FROM flight WHERE flight_number=%s and departure_date_time=%s " \
                "and airline_name=%s"
        cursor.execute(query, (flight_number, dep_date, airline_name))
        base_price = cursor.fetchone()["base_price"]
        query = 'INSERT INTO buy VALUES(%s,%s,now(),%s,%s,%s,%s, %s)'
        if remain / num_seats <= 0.25:
            cursor.execute(query,
                           (ticket_id, username, name_on_card, card_num, card_type, expir_date, base_price * 1.25))
        else:
            cursor.execute(query, (ticket_id, username, name_on_card, card_num, card_type, expir_date, base_price))
        query = "select email from rate where email = %s and airline_name = %s and departure_date_time = %s and flight_number = %s"
        cursor.execute(query, (username, airline_name, dep_date, flight_number))
        data1 = cursor.fetchall()
        if (not data1):
            query = "INSERT INTO rate VALUES(%s,%s,%s,%s,Null,Null)"
            cursor.execute(query, (username, airline_name, dep_date, flight_number))
        cursor.close()
        return render_template('customer_home.html', username=username, success="Successful buy tickets")


@app.route('/comment_and_rate', methods=['GET', 'POST'])
def comment_and_rate():
    username = session['username']
    flight_number = request.form["flight_number"]
    airline_name = request.form["airline_name"]
    dep_date = request.form["departure_date"]
    dep_date = dep_date.replace("T", " ") + ":00"
    comment = request.form["comment"]
    rate = request.form["rate"]
    cursor = conn.cursor()
    query = "SELECT flight_number,departure_date_time,airline_name FROM flight " \
            "WHERE flight_number=%s and airline_name = %s and departure_date_time =%s"
    cursor.execute(query, (flight_number, airline_name, dep_date))
    data = cursor.fetchall()
    if (not data):
        error = "Please check the flight information"
        return render_template('customer_home.html', username=username, error3=error)
    query = "SELECT flight_number,departure_date_time,airline_name FROM rate " \
            "WHERE flight_number=%s and airline_name = %s and departure_date_time =%s and email=%s and comment is not Null"
    cursor.execute(query, (flight_number, airline_name, dep_date, username))
    data = cursor.fetchall()
    if (data):
        error = "You have already commented or rated this flight"
        return render_template('customer_home.html', username=username, error3=error)
    query = 'UPDATE rate SET rating=%s, comment=%s WHERE email=%s and airline_name=%s and departure_date_time=%s and flight_number=%s'
    cursor.execute(query, (rate, comment, username, airline_name, dep_date, flight_number))
    cursor.close()
    return render_template('customer_home.html', username=username, success="Successful rate and commented")


@app.route('/track_spending', methods=['GET', 'POST'])
def track_spending():
    username = session["username"]
    start_date = request.form["start_date"]
    end_date = request.form["end_date"]
    cursor = conn.cursor()
    query = "SELECT sum(case when b.price is not null then b.price else 0 end) as total_spend, " \
            "a.year, a.month from (select distinct year(date) as year, month(date) as month " \
            "from calendar where date between %s and %s group by month)as a " \
            "left join (select * from buy where email = %s and date(purchase_date_time) between %s and %s)as b " \
            "on a.year = year(b.purchase_date_time) and a.month = month(b.purchase_date_time) group by year,month Order by year, month desc"
    cursor.execute(query, (start_date, end_date, username, start_date, end_date))
    cursor.close()
    data1 = cursor.fetchall()
    if not data1:
        return render_template('customer_home.html', username=username, error4="No Spend found", start_date=start_date,
                               end_date=end_date)
    else:
        return render_template('customer_home.html', username=username, track_spend=data1, start_date=start_date,
                               end_date=end_date)


# TODO: check
def get_airline_name():
    username = session["username"]
    cursor = conn.cursor()
    query = "SELECT airline_name FROM staff WHERE username = %s"
    cursor.execute(query, (username))
    data = cursor.fetchone()
    cursor.close()
    return data["airline_name"]


@app.route("/staff_home")
def staff_home():
    username, data1, data2, data3, sum_month, sum_year, email, data6, data7 = get_staff_home_data()
    return render_template('staff_home.html', username=username, airline_fights=data1, destination_3_months=data2,
                           destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                           customer_name=email, customer_flights=data6, owned_airplane=data7)


def get_staff_home_data():
    username = session['username']
    airline = get_airline_name()
    cursor = conn.cursor()
    query = "SELECT flight_number,departure_date_time,airline_name " \
            "FROM staff natural join airline natural join flight " \
            "WHERE username = %s and departure_date_time between now() and (SELECT DATE_ADD(now(), INTERVAL 30 DAY))" \
            "ORDER BY departure_date_time DESC"
    cursor.execute(query, (username))
    data1 = cursor.fetchall()
    # 小于3个月 (last 3 month)
    query = "SELECT city, count(*) AS count " \
            "FROM buy natural join ticket natural join flight join airport on (arrive_airport_code=code)" \
            "WHERE airline_name = %s and purchase_date_time between (SELECT DATE_ADD(now(), INTERVAL-12 MONTH )) and now()" \
            "GROUP BY city ORDER BY count DESC LIMIT 3"
    cursor.execute(query, (airline))
    data2 = cursor.fetchall()
    # 过去一年 (last 1 year)
    query = "SELECT city, count(*) AS count " \
            "FROM buy natural join ticket natural join flight join airport on (arrive_airport_code=code)" \
            "WHERE airline_name = %s and purchase_date_time between (SELECT DATE_ADD(now(), INTERVAL-1 YEAR )) and now()" \
            "GROUP BY city ORDER BY count DESC LIMIT 3"
    cursor.execute(query, (airline))
    data3 = cursor.fetchall()
    # 找ticket的价格 (上个月)
    query = "SELECT sum(price) AS sum FROM buy natural join ticket WHERE airline_name=%s and " \
            "purchase_date_time between (SELECT DATE_ADD(now(), INTERVAL-1 MONTH )) and now()"
    cursor.execute(query, (airline))
    sum_month = cursor.fetchone()["sum"]
    # 找ticket的价格 (上一年)
    query = "SELECT sum(price) AS sum FROM buy natural join ticket WHERE airline_name=%s and " \
            "purchase_date_time between (SELECT DATE_ADD(now(), INTERVAL-1 YEAR )) and now()"
    cursor.execute(query, (airline))
    sum_year = cursor.fetchone()["sum"]
    # most frequent customer
    query = "SELECT count(*) as count, email FROM buy GROUP BY email ORDER BY count DESC LIMIT 1"
    cursor.execute(query)
    email=cursor.fetchone()
    if (email==None):
        email = "No Customer Buy Tickets for this Airline"
    else:
        email = email["email"]
    query = "SELECT flight_number, departure_date_time " \
            "FROM buy natural join ticket WHERE email = %s and airline_name=%s"
    cursor.execute(query, (email, airline))
    data6 = cursor.fetchall()
    query = "SELECT airplane_id,num_seats FROM airplane WHERE airline_name =%s"
    cursor.execute(query, (airline))
    data7 = cursor.fetchall()
    cursor.close()
    return (username, data1, data2, data3, sum_month, sum_year, email, data6, data7)


# TODO:check
@app.route('/search_flights_staff', methods=['GET', 'POST'])
def search_flights_staff():
    username, data1, data2, data3, sum_month, sum_year, email, data6, data7 = get_staff_home_data()
    airline_name = get_airline_name()
    start_date = request.form["start_date"]
    end_date = request.form["end_date"]
    error = Auth_staff()
    if (error != None):
        return render_template("staff_home.html", error8=error, username=username, airline_fights=data1,
                               destination_3_months=data2,
                               destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                               customer_name=email, customer_flights=data6, owned_airplane=data7)
    query = "SELECT flight_number, departure_date_time FROM flight " \
            "WHERE airline_name=%s and date(departure_date_time)>=%s and date(departure_date_time)<=%s"
    cursor = conn.cursor()
    cursor.execute(query, (airline_name, start_date, end_date))
    data = cursor.fetchall()
    if (not data):
        return render_template("staff_home.html", search_flights=data, username=username, airline_fights=data1,
                               destination_3_months=data2,
                               destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                               customer_name=email, customer_flights=data6, owned_airplane=data7,
                               post1="No Flight Found")
    return render_template("staff_home.html", search_flights=data, username=username, airline_fights=data1,
                           destination_3_months=data2,
                           destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                           customer_name=email, customer_flights=data6, owned_airplane=data7)


@app.route('/create_new_airport', methods=['GET', 'POST'])
def create_new_airport():
    username, data1, data2, data3, sum_month, sum_year, email, data6, data7 = get_staff_home_data()
    code = request.form['code']
    airport_name = request.form['airport_name']
    city = request.form["city"]
    error = Auth_staff()
    if (error != None):
        return render_template('staff_home.html', error2=error, username=username, airline_fights=data1,
                               destination_3_months=data2,
                               destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                               customer_name=email, customer_flights=data6, owned_airplane=data7)
    cursor = conn.cursor()
    query = 'SELECT * FROM airport WHERE code = %s'
    cursor.execute(query, (code))
    data = cursor.fetchone()
    if (data):
        error = "That code for airport has already existed"
        return render_template('staff_home.html', error2=error, username=username, airline_fights=data1,
                               destination_3_months=data2,
                               destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                               customer_name=email, customer_flights=data6, owned_airplane=data7)

    query = 'INSERT INTO airport VALUES(%s,%s,%s)'
    cursor.execute(query, (code, airport_name, city))
    return render_template("staff_home.html", success="Successful added Airport", username=username,
                           airline_fights=data1,
                           destination_3_months=data2,
                           destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                           customer_name=email, customer_flights=data6, owned_airplane=data7)


@app.route('/create_new_airplane', methods=['GET', 'POST'])
def create_new_airplane():
    username, data1, data2, data3, sum_month, sum_year, email, data6, data7 = get_staff_home_data()
    username = session["username"]
    airline_name = get_airline_name()
    id = request.form['id']
    num_seats = request.form["num_seats"]
    error = Auth_staff()
    if (error != None):
        return render_template('staff_home.html', error3=error, username=username, airline_fights=data1,
                               destination_3_months=data2,
                               destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                               customer_name=email, customer_flights=data6, owned_airplane=data7)
    cursor = conn.cursor()
    query = 'SELECT * FROM airline WHERE airline_name = %s'
    cursor.execute(query, (airline_name))
    data = cursor.fetchone()
    if (not data):
        error = "That airline does not exist"
        return render_template('staff_home.html', error3=error, username=username, airline_fights=data1,
                               destination_3_months=data2,
                               destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                               customer_name=email, customer_flights=data6, owned_airplane=data7)
    query = 'SELECT * FROM airplane WHERE airline_name = %s and airplane_id = %s'
    cursor.execute(query, (airline_name, id))
    data = cursor.fetchone()
    if (data):
        error = "That code of airplane has already existed for that airline"
        return render_template('staff_home.html', error3=error, username=username, airline_fights=data1,
                               destination_3_months=data2,
                               destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                               customer_name=email, customer_flights=data6, owned_airplane=data7)
    query = 'INSERT INTO airplane VALUES(%s,%s,%s)'
    cursor.execute(query, (airline_name, id, num_seats))
    username, data1, data2, data3, sum_month, sum_year, email, data6, data7 = get_staff_home_data()
    return render_template("staff_home.html", success="Successful added airplane", username=username,
                           airline_fights=data1,
                           destination_3_months=data2,
                           destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                           customer_name=email, customer_flights=data6, owned_airplane=data7)


@app.route('/create_new_flights', methods=['GET', 'POST'])
def create_new_flights():
    username, data1, data2, data3, sum_month, sum_year, email, data6, data7 = get_staff_home_data()
    flight_number = request.form['flight_number']
    airline_name = get_airline_name()
    dep_date = request.form["departure_date"]
    dep_date = dep_date.replace("T", " ") + ":00"
    arrival_date = request.form["arrival_date"]
    arrival_date = arrival_date.replace("T", " ") + ":00"
    base_price = request.form['base_price']
    airplane_id = request.form['airplane_id']
    depart_airport_code = request.form["depart_airport_code"]
    arrival_airport_code = request.form["arrive_airport_code"]
    status = request.form["status"]
    error = Auth_staff()
    if (error != None):
        return render_template('staff_home.html', error4=error, username=username, airline_fights=data1,
                               destination_3_months=data2,
                               destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                               customer_name=email, customer_flights=data6, owned_airplane=data7)
    cursor = conn.cursor()
    query = "SELECT flight_number,departure_date_time,airline_name FROM flight " \
            "WHERE flight_number=%s and airline_name = %s and departure_date_time =%s"
    cursor.execute(query, (flight_number, airline_name, dep_date))
    data = cursor.fetchall()
    if (data):
        error = "Please check flight information it repeat with other flights"
        return render_template('staff_home.html', error4=error, username=username, airline_fights=data1,
                               destination_3_months=data2,
                               destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                               customer_name=email, customer_flights=data6, owned_airplane=data7)
    query = "SELECT * FROM airplane WHERE airplane_id = %s and airline_name=%s"
    cursor.execute(query, (airplane_id, airline_name))
    if (not cursor.fetchone()):
        error = "Airplane ID not exist for this airline"
        return render_template('staff_home.html', error4=error, username=username, airline_fights=data1,
                               destination_3_months=data2,
                               destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                               customer_name=email, customer_flights=data6, owned_airplane=data7)
    query = "SELECT code FROM airport where code=%s"
    cursor.execute(query, (depart_airport_code))
    data = cursor.fetchall()
    if (not data):
        error = "Departure airport code not exist"
        return render_template('staff_home.html', username=username, error4=error, airline_fights=data1,
                               destination_3_months=data2,
                               destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                               customer_name=email, customer_flights=data6, owned_airplane=data7)
    query = "SELECT code FROM airport where code=%s"
    cursor.execute(query, (arrival_airport_code))
    data = cursor.fetchall()
    if (not data):
        error = "Arrival airport code not exist"
        return render_template('staff_home.html', username=username, error4=error, airline_fights=data1,
                               destination_3_months=data2,
                               destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                               customer_name=email, customer_flights=data6, owned_airplane=data7)
    query = "INSERT INTO flight VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (
        flight_number, dep_date, airline_name, arrival_date, base_price, status, airplane_id, depart_airport_code,
        arrival_airport_code))
    query = "SELECT max(ticket_id) AS max FROM ticket"
    cursor.execute(query)
    ticket_id_max=cursor.fetchone()
    if (not ticket_id_max):
        ticket_id_max = 0
    else:
        ticket_id_max = int(ticket_id_max["max"])
    query = "SELECT num_seats FROM airplane WHERE airplane_id=%s"
    cursor.execute(query, airplane_id)
    num_seats = cursor.fetchone()["num_seats"]
    query = "INSERT INTO ticket VALUES(%s,%s,%s,%s)"
    for num in range(1, num_seats + 1):
        new_ticket_id = ticket_id_max + num
        new_ticket_id = str(new_ticket_id).rjust(20, "0")
        cursor.execute(query, (new_ticket_id, flight_number, dep_date, airline_name))
    username, data1, data2, data3, sum_month, sum_year, email, data6, data7 = get_staff_home_data()
    return render_template("staff_home.html", success="Successful added flight", username=username,
                           airline_fights=data1,
                           destination_3_months=data2,
                           destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                           customer_name=email, customer_flights=data6, owned_airplane=data7)


# TODO: check
@app.route('/change_status', methods=['GET', 'POST'])
def change_status():
    username, data1, data2, data3, sum_month, sum_year, email, data6, data7 = get_staff_home_data()
    flight_number = request.form['flight_number']
    airline_name = get_airline_name()
    dep_date = request.form["departure_date"]
    dep_date = dep_date.replace("T", " ") + ":00"
    status = request.form["status"]
    error = Auth_staff()
    if (error != None):
        return render_template('staff_home.html', error5=error, username=username, airline_fights=data1,
                               destination_3_months=data2,
                               destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                               customer_name=email, customer_flights=data6, owned_airplane=data7)
    cursor = conn.cursor()
    query = "SELECT flight_number,departure_date_time,airline_name FROM flight " \
            "WHERE flight_number=%s and airline_name = %s and departure_date_time =%s"
    cursor.execute(query, (flight_number, airline_name, dep_date))
    data = cursor.fetchall()
    if (not data):
        error = "No flight founded, please check your flight information"
        return render_template('staff_home.html', username=username, error5=error, airline_fights=data1,
                               destination_3_months=data2,
                               destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                               customer_name=email, customer_flights=data6, owned_airplane=data7)
    query = "UPDATE flight SET status = %s WHERE flight_number=%s and departure_date_time=%s and airline_name=%s"
    cursor.execute(query, (status, flight_number, dep_date, airline_name))
    cursor.close()
    return render_template("staff_home.html", success="Successful change status", username=username,
                           airline_fights=data1,
                           destination_3_months=data2,
                           destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                           customer_name=email, customer_flights=data6, owned_airplane=data7)


@app.route('/view_reports', methods=['GET', 'POST'])
def view_reports():
    username, data1, data2, data3, sum_month, sum_year, email, data6, data7 = get_staff_home_data()
    start_date = request.form["start_date"]
    end_date = request.form["end_date"]
    error = Auth_staff()
    if (error != None):
        return render_template('staff_home.html', error6=error, username=username, airline_fights=data1,
                               destination_3_months=data2,
                               destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                               customer_name=email, customer_flights=data6, owned_airplane=data7)
    cursor = conn.cursor()
    # TODO: 每个月的!!!!


@app.route('/view_rating', methods=['GET', 'POST'])
def view_rating():
    username, data1, data2, data3, sum_month, sum_year, email, data6, data7 = get_staff_home_data()
    error = Auth_staff()
    if (error != None):
        return render_template("staff_home.html", error7=error, username=username, airline_fights=data1,
                               destination_3_months=data2,
                               destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                               customer_name=email, customer_flights=data6, owned_airplane=data7)
    flight_number = request.form['flight_number']
    airline_name = get_airline_name()
    dep_date = request.form["departure_date"]
    dep_date = dep_date.replace("T", " ") + ":00"
    cursor = conn.cursor()
    query = 'SELECT avg(rating) AS avg FROM rate WHERE flight_number = %s and departure_date_time = %s and airline_name=%s and comment is not Null'
    cursor.execute(query, (flight_number, dep_date, airline_name))
    data = cursor.fetchone()
    if (data["avg"] == None):
        return render_template("staff_home.html", post3="No Rating and Comment for this Flight", rating_comment=data,
                               username=username,
                               airline_fights=data1,
                               destination_3_months=data2,
                               destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                               customer_name=email, customer_flights=data6, owned_airplane=data7)
    avg = format(data["avg"], ".2f")
    query = "SELECT rating, comment FROM rate WHERE flight_number = %s and departure_date_time = %s and airline_name=%s and comment is not Null"
    cursor.execute(query, (flight_number, dep_date, airline_name))
    data = cursor.fetchall()
    # print(data,avg)
    return render_template("staff_home.html", average=avg, rating_comment=data, username=username, airline_fights=data1,
                           destination_3_months=data2,
                           destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                           customer_name=email, customer_flights=data6, owned_airplane=data7)


@app.route('/find_customer', methods=['GET', 'POST'])
def find_customer():
    username, data1, data2, data3, sum_month, sum_year, email, data6, data7 = get_staff_home_data()
    flight_number = request.form['flight_number']
    airline_name = get_airline_name()
    dep_date = request.form["departure_date"]
    error = Auth_staff()
    if (error != None):
        return render_template('staff_home.html', error1=error, username=username, airline_fights=data1,
                               destination_3_months=data2,
                               destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                               customer_name=email, customer_flights=data6, owned_airplane=data7)
    cursor = conn.cursor()
    query = "SELECT flight_number,departure_date_time,airline_name FROM flight " \
            "WHERE flight_number=%s and airline_name = %s and departure_date_time =%s"
    cursor.execute(query, (flight_number, airline_name, dep_date))
    data = cursor.fetchall()
    if (not data):
        error = "Please check the flight information"
        return render_template('staff_home.html', username=username, error1=error, airline_fights=data1,
                               destination_3_months=data2,
                               destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                               customer_name=email, customer_flights=data6, owned_airplane=data7)

    query = "SELECT name, phone_number " \
            "FROM customer natural join buy natural join ticket natural join flight " \
            "WHERE flight_number=%s and airline_name = %s and departure_date_time =%s"
    cursor.execute(query, (flight_number, airline_name, dep_date))
    data = cursor.fetchall()
    if (not data):
        return render_template("staff_home.html", customers=data, username=username, airline_fights=data1,
                               destination_3_months=data2,
                               destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                               customer_name=email, customer_flights=data6, owned_airplane=data7,
                               post2="No Customer in the Flight")
    return render_template("staff_home.html", customers=data, username=username, airline_fights=data1,
                           destination_3_months=data2,
                           destination_year=data3, sum_month=sum_month, sum_year=sum_year,
                           customer_name=email, customer_flights=data6, owned_airplane=data7)


# TODO: 放到每个的最开始
def Auth_staff():
    username = session["username"]
    cursor = conn.cursor()
    query = 'SELECT * FROM staff WHERE username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    error = None
    if (not data): error = "No authentication for this action"
    cursor.close()
    return error


# Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    # grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    # check whether it is staff
    isStaff = False
    # cursor used to send queries
    cursor = conn.cursor()
    # executes query (check for customer)
    query = 'SELECT * FROM customer WHERE email = %s and password = md5(%s)'
    cursor.execute(query, (username, password))
    # stores the results in a variable
    data = cursor.fetchone()
    if (not data):
        isStaff = True
        query = 'SELECT * FROM staff WHERE username = %s and password = md5(%s)'
        cursor.execute(query, (username, password))
        # stores the results in a variable
        data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if (data):
        # creates a session for the user
        # session is a built in
        session['username'] = username
        if (isStaff):
            # TODO: homepage build for staff
            return redirect(url_for('staff_home'))
        else:
            # TODO: homepage build for customer
            return redirect(url_for('customer_home', if_initial=1))
    else:
        # returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login.html', error=error)


@app.route('/registerAuth_staff', methods=['GET', 'POST'])
def registerAuth_staff():
    # TODO
    username = request.form['username']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']
    airline_name = request.form['airline_name']
    cursor = conn.cursor()
    query = 'SELECT * FROM staff WHERE username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    error = "Error with the input"
    if (data):
        # If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register_staff.html', error=error)
    else:
        ins = 'INSERT INTO staff VALUES(%s, md5(%s), %s, %s,%s, %s)'
        cursor.execute(ins, (username, password, first_name, last_name, date_of_birth, airline_name))
        conn.commit()
        cursor.close()
        return render_template('login.html')


@app.route('/registerAuth_customer', methods=['GET', 'POST'])
def registerAuth_customer():
    email = request.form['username']
    name = request.form['name']
    password = request.form['password']
    building_number = request.form['building_number']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    phone_number = request.form['phone_number']
    passport_number = request.form['passport_number']
    passport_expiration = request.form['passport_expiration']
    passport_country = request.form['passport_country']
    date_of_birth = request.form['date_of_birth']
    cursor = conn.cursor()
    query = 'SELECT * FROM customer WHERE email = %s'
    cursor.execute(query, (email))
    data = cursor.fetchone()
    error = "Error with the information typed in"
    if (data):
        # If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register_customer.html', error=error)
    else:
        ins = 'INSERT INTO Customer VALUES(%s, %s, md5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (
            email, name, password, building_number, street, city, state, phone_number, passport_number,
            passport_expiration,
            passport_country, date_of_birth))
        conn.commit()
        cursor.close()
        return render_template('login.html')


# customer login behave

# staff login behave

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')


app.secret_key = 'some key that you will never guess'
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)

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
        query = "SELECT e.flight_number, date(e.departure_date_time) as departure_date, e.airline_name, " \
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
        query = 'SELECT b.flight_number, b.departure_date, b.airline_name, ""as return_flight_number, "" as return_date, ""as return_airline_name ' \
                'FROM Airport as a join (select flight_number, date(departure_date_time) ' \
                'as departure_date, airline_name, depart_airport_code, arrive_airport_code from Flight)as b ' \
                'on b.depart_airport_code=a.code join Airport as c on b.arrive_airport_code=c.code WHERE a.city= %s ' \
                'and a.name=%s and c.city=%s and c.name=%s and b.departure_date = %s'
        cursor.execute(query, (source_city, source_airport, des_city, des_airport, date))
    data = cursor.fetchall()
    cursor.close()
    ##error = "Error with the input"
    if (len(data) == 0):
        error = "No flight founded, please check your flight information"
        return render_template("index.html", error1=error)
        ##error = "Error with the input"
    return render_template("index.html", posts1=data)


@app.route('/flight_search_home', methods=['GET', 'POST'])
def flight_search_home():
    source_city = request.form['source_city']
    source_airport = request.form['source_airport']
    des_city = request.form['des_city']
    des_airport = request.form['des_airport']
    date = request.form["departure_date"]
    cursor = conn.cursor()
    query = 'SELECT b.flight_number, b.departure_date, b.airline_name ' \
            'FROM Airport as a join (select flight_number, date(departure_date_time) ' \
            'as departure_date, airline_name, depart_airport_code, arrive_airport_code from Flight)as b ' \
            'on b.depart_airport_code=a.code join Airport as c on b.arrive_airport_code=c.code WHERE a.city= %s ' \
            'and a.name=%s and c.city=%s and c.name=%s and b.departure_date = %s'
    cursor.execute(query, (source_city, source_airport, des_city, des_airport, date))
    data = cursor.fetchall()
    cursor.close()
    ##error = "Error with the input"
    if (len(data) == 0):
        error = "No flight founded, please check your flight information"
        return render_template("customer_home.html", error1=error)
        ##error = "Error with the input"
    return render_template("customer_home.html", Search_flight=data)


@app.route('/See_status', methods=['GET', 'POST'])
def See_status():
    # TODO: check
    airline_name = request.form['airline_name']
    flight_number = request.form['flight_number']
    arrival_date = request.form['arrival_date']
    departure_date = request.form['departure_date']
    # time_format = '%Y-%m-%dT%H:%M:%S'
    # arrival_date=time.strptime(arrival_date+":00",time_format)
    # departure_date=time.strptime(departure_date+":00",time_format)
    # print(arrival_date)
    # print()
    cursor = conn.cursor()
    query = 'SELECT a.status FROM ' \
            '(select status, flight_number, date(departure_date_time) as departure_date, ' \
            'date(arrival_date_time) as arrival_date, airline_name from flight)as a ' \
            'WHERE a.flight_number = %s and a.departure_date=%s and a.airline_name=%s ' \
            'and a.arrival_date=%s'
    cursor.execute(query, (flight_number, departure_date, airline_name, arrival_date))
    data = cursor.fetchall()
    cursor.close()
    if (len(data) == 0):
        error = "No flight founded, please check your flight information"
        return render_template("index.html", error2=error)
    ##error = "Error with the input"
    return render_template("index.html", posts2=data)


@app.route('/customer_home/<int:if_initial>', methods=['GET', 'POST'])
def customer_home(if_initial):
    username = session['username']
    cursor = conn.cursor()
    if if_initial == 0:
        flight_type = request.form['flight_type']
    else:
        flight_type = "Future"
    if flight_type == "All":
        query = "SELECT flight_number,departure_date_time as dep,airline_name " \
                "FROM customer natural join buy natural join ticket " \
                "WHERE email = %s ORDER BY departure_date_time DESC"
    elif flight_type == "Past":
        query = "SELECT flight_number,departure_date_time as dep,airline_name " \
                "FROM customer natural join buy natural join ticket " \
                "WHERE email = %s and departure_date_time < now() ORDER BY departure_date_time DESC"
    else:
        query = "SELECT flight_number,departure_date_time as dep,airline_name " \
                "FROM customer natural join buy natural join ticket " \
                "WHERE email = %s and departure_date_time >= now() ORDER BY departure_date_time DESC"
    cursor.execute(query, (username))
    data1 = cursor.fetchall()
    cursor.close()
    return render_template('customer_home.html', username=username, future_flight=data1, flight_type=flight_type)


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
    dep_date=dep_date.replace("T"," ")+":00"
    ##TODO: 怎么找到future
    query = "SELECT flight_number,departure_date_time,airline_name FROM flight WHERE flight_number= %s and airline_name = %s and departure_date_time = %s"
    cursor.execute(query, (flight_number, airline_name, dep_date))
    data = cursor.fetchall()
    if (not data):
        error = "Please check the flight information"
        return render_template('customer_home.html', username=username, error2=error)
    query="SELECT ticket_id FROM ticket WHERE flight_number=%s and departure_date_time=%s and airline_name=%s and ticket_id not in buy LIMIT 1"
    cursor.execute(query, (flight_number, airline_name, dep_date))
    ticket_id=cursor.fetchone()[0]
    query = 'INSERT INTO buy VALUES(%s,%s,now(),%s,%s,%s,%s)'
    cursor.execute(query,(ticket_id,username,name_on_card,card_num,card_type))
    cursor.close()
    return render_template('customer_home.html', username=username, success="Successful buy tickets")


@app.route('/comment_and_rate', methods=['GET', 'POST'])
def comment_and_rate():
    username = session['username']
    flight_number = request.form["flight_number"]
    airline_name = request.form["airline_name"]
    dep_date = request.form["departure_date"]
    dep_date=dep_date.replace("T"," ")+":00"
    comment = request.form["comment"]
    # TODO: 有可能是str的形式 sql里是numeric(2,1)
    rate = request.form["rate"]
    cursor = conn.cursor()
    query = "SELECT flight_number,departure_date_time,airline_name " \
            "FROM flight" \
            "WHERE flight_number=%s and airline_name = %s and departure_date_time =%s"
    cursor.execute(query, (flight_number, airline_name, dep_date))
    data = cursor.fetchall()
    if (not data):
        error = "Please check the flight information"
        return render_template('customer_home.html', username=username, error3=error)
    query = "SELECT flight_number,departure_date_time,airline_name " \
            "FROM rate" \
            "WHERE flight_number=%s and airline_name = %s and departure_date_time =%s and email=%s"
    cursor.execute(query, (flight_number, airline_name, dep_date, username))
    data = cursor.fetchall()
    if (data):
        error = "You have already commented or rated this flight"
        return render_template('customer_home.html', username=username, error3=error)
    query = 'INSERT INTO rate VALUES(%s,%s,%s,%s,%s,%s)'
    cursor.execute(query, (username, airline_name, dep_date, flight_number, rate, comment))
    cursor.close()
    return render_template('customer_home.html', username=username, success="Successful rate and commented")

@app.route('/track_spending', methods=['GET', 'POST'])
def track_spending():
    username=session["username"]
    start_date=request.form["start_date"]
    end_date=request.form["end_date"]

# TODO: check
def get_airline_name():
    username = session["username"]
    cursor = conn.cursor()
    query = "SELECT airline_name FROM staff WHERE username = %s"
    cursor.execute(query, (username))
    data = cursor.fetchone()
    cursor.close()
    return data[0][0]


# TODO: check
@app.route('/staff_home')
def staff_home():
    username = session['username']
    airline = get_airline_name()
    cursor = conn.cursor()
    query = "SELECT flight_number,departure_date_time,airline_name " \
            "FROM staff natural join airline natural join flight " \
            "WHERE username = %s and departure_date_time between (SELECT DATE_ADD (now(), INTERVAL +30 DAY)) and now()" \
            "ORDER BY departure_date_time DESC"
    cursor.execute(query, (username))
    data1 = cursor.fetchall()
    # 小于3个月 (last 3 month)
    query = "SELECT city, count(*) AS count " \
            "FROM buy natural join ticket natural join flight join airport using (arrive_airport_code=code)" \
            "WHERE airline_name = %s and purchase_date_time between (SELECT DATE_ADD(now(), INTERVAL-12 MONTH )) and now()" \
            "GROUP BY city ORDER BY count DESC LIMIT 3"
    cursor.execute(query, (airline))
    data2 = cursor.fetchall()
    # 过去一年 (last 1 year)
    query = "SELECT city, count(*) AS count " \
            "FROM buy natural join ticket natural join flight join airport using (arrive_airport_code=code)" \
            "WHERE airline_name = %s and purchase_date_time between (SELECT DATE_ADD(now(), INTERVAL-1 YEAR )) and now()" \
            "GROUP BY city ORDER BY count DESC LIMIT 3"
    cursor.execute(query, (airline))
    data3 = cursor.fetchall()
    # 找ticket的价格 (上个月)
    query = "SELECT count(ticket_id) AS count, base_price, num_seats" \
            "FROM buy natural join ticket natural join flight natural join airplane" \
            "WHERE airline_name = %s and purchase_date_time between (SELECT DATE_ADD(now(), INTERVAL-1 MONTH )) and now()" \
            "GROUP BY flight_number,departure_date_time,airline_name"
    cursor.execute(query, (airline))
    data4 = cursor.fetchall()
    sum_month = 0
    for row in data4:
        count = row[0]
        base_price = row[1]
        num_seats = row[2]
        if (count > num_seats * 0.75):
            normal = int(num_seats * 0.75)
            sum_month += (normal * base_price + (count - normal) * (base_price * 1.25))
        else:
            sum_month += count * base_price
    # 找ticket的价格 (上一年)
    query = "SELECT count(ticket_id) AS count, base_price, num_seats" \
            "FROM buy natural join ticket natural join flight natural join airplane" \
            "WHERE airline_name = %s and purchase_date_time between (SELECT DATE_ADD(now(), INTERVAL-1 YEAR )) and now()" \
            "GROUP BY flight_number,departure_date_time,airline_name"
    cursor.execute(query, (airline))
    data5 = cursor.fetchall()
    sum_year = 0
    for row in data5:
        count = row[0]
        base_price = row[1]
        num_seats = row[2]
        if (count > num_seats * 0.75):
            normal = int(num_seats * 0.75)
            sum_year += (normal * base_price + (count - normal) * (base_price * 1.25))
        else:
            sum_year += count * base_price
    # most frequent customer
    query = "SELECT count(*) as count, email AS count FROM buy GROUP BY email ORDER BY count DESC LIMIT 1"
    cursor.execute(query)
    email = cursor.fechall()["email"]
    query = "SELECT flight_number, departure_date_time, airline_name" \
            "FROM buy natural join ticket " \
            "WHERE email = %s"
    cursor.execute(query, (email))
    data6 = cursor.fetchall()
    query = "SELECT id,num_seats FROM airplane WHERE airline_name =%s"
    cursor.execute(query, (email))
    data7 = cursor.fecthall()
    cursor.close()
    return render_template('staff_home.html', username=username, airline_fights=data1, destination_3_months=data2,
                           destination_year=data3, revenue_last_month=[sum_month], revenue_last_year=[sum_year],
                           customer_name=email, customer_flights=data6, owned_airplane=data7)


@app.route('/create_new_airport', methods=['GET', 'POST'])
def create_new_airport():
    username = session["username"]
    code = request.form['code']
    airport_name = request.form['airport_name']
    city = request.form["city"]
    cursor = conn.cursor()
    query = 'SELECT * FROM staff WHERE username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    error = None
    if (not data):
        error = "No authentication for this action"
        return render_template('staff_home.html', error2=error)
    else:
        query = 'SELECT * FROM airport WHERE code = %s'
        cursor.execute(query, (code))
        data = cursor.fetchone()
        if (data):
            error = "That code for airport has already existed"
            return render_template('staff_home.html', error2=error)
        else:
            query = 'INSERT INTO airport VALUES(%s,%s,%s)'
            cursor.execute(query, (code, airport_name, city))
        return render_template("staff_home.html", success="Successful added Airport")


@app.route('/create_new_airplane', methods=['GET', 'POST'])
def create_new_airplane():
    username = session["username"]
    airline_name = get_airline_name()
    id = request.form['id']
    num_seats = request.form["num_seats"]
    cursor = conn.cursor()
    query = 'SELECT * FROM staff WHERE username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    error = None
    if (not data):
        error = "No authentication for this action"
        return render_template('staff_home.html', error3=error)
    else:
        query = 'SELECT * FROM airline WHERE airline_name = %s'
        cursor.execute(query, (airline_name))
        data = cursor.fetchone()
        if (not data):
            error = "That airline does not exist"
            return render_template('staff_home.html', error3=error)
        else:
            query = 'SELECT * FROM airplane WHERE airline_name = %s and airplane_id = %s'
            cursor.execute(query, (airline_name, id))
            data = cursor.fetchone()
            if (data):
                error = "That code of airplane has already existed for that airline"
                return render_template('staff_home.html', error3=error)
            else:
                query = 'INSERT INTO airplane VALUES(%s,%s,%s)'
                cursor.execute(query, (airline_name, id, num_seats))
                return render_template("staff_home.html", success="Successful added airplane")


@app.route('/create_new_flights', methods=['GET', 'POST'])
def create_new_flights():
    username = session["username"]
    flight_number = request.form['flight_number']
    airline_name = get_airline_name()
    dep_date = request.form["departure_date"]
    dep_date=dep_date.replace("T"," ")+":00"
    arrival_date = request.form["arrival_date"]
    arrival_date=arrival_date.replace("T"," ")+":00"
    base_price = request.form['base_price']
    airplane_id = request.form['airplane_id']
    depart_airport_code = request.form["depart_airport_code"]
    arrival_airport_code = request.form["arrival_airport_code"]
    status = request.form["status"]
    cursor = conn.cursor()
    query = 'SELECT * FROM staff WHERE username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    if (not data):
        error = "No authentication for this action"
        return render_template('staff_home.html', error4=error)
    query = "SELECT flight_number,departure_date_time,airline_name " \
            "FROM flight" \
            "WHERE flight_number=%s and airline_name = %s and departure_date_time =%s"
    cursor.execute(query, (flight_number, airline_name, dep_date))
    data = cursor.fetchall()
    if (data):
        error = "Please check flight information it repeat with other flights"
        return render_template('staff_home.html', username=username, error4=error)
    query = "SELECT code FROM airport where code=%s"
    cursor.execute(query, (depart_airport_code))
    data = cursor.fetchall()
    if (not data):
        error = "Departure airport code not exist"
        return render_template('staff_home.html', username=username, error4=error)
    query = "SELECT code FROM airport where code=%s"
    cursor.execute(query, (arrival_airport_code))
    data = cursor.fetchall()
    if (not data):
        error = "Arrival airport code not exist"
        return render_template('staff_home.html', username=username, error4=error)
    query = "INSERT INTO flight VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (
        flight_number, dep_date, airline_name, arrival_date, base_price, status, airplane_id, depart_airport_code,
        arrival_airport_code))
    query="SELECT max(ticket_id)GROUP FROM ticket"
    cursor.execute(query)
    ticket_id_max=int(cursor.fetchone()[0])
    query="SELECT num_seats FROM airplane WHERE airplane_id=%s"
    cursor.execute(query,airplane_id)
    num_seats=cursor.fetchone()[0]
    query="INSERT INTO ticket VALUES(%s,%s,%s,%s)"
    for num in range(1,num_seats+1):
        new_ticket_id=ticket_id_max+num
        new_ticket_id=str(new_ticket_id).rjust(20,"0")
        cursor.execute(query,(new_ticket_id,flight_number,dep_date,airline_name))
    return render_template("staff_home.html", success="Successful added flight")


# TODO: check
@app.route('/change_status', methods=['GET', 'POST'])
def change_status():
    username = session["username"]
    flight_number = request.form['flight_number']
    airline_name = get_airline_name()
    dep_date = request.form["departure_date"]
    dep_date=dep_date.replace("T"," ")+":00"
    status = request.form["status"]
    cursor = conn.cursor()
    query = 'SELECT * FROM staff WHERE username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    if (not data):
        error = "No authentication for this action"
        return render_template('staff_home.html', error5=error)
    query = "SELECT flight_number,departure_date_time,airline_name " \
            "FROM flight" \
            "WHERE flight_number=%s and airline_name = %s and departure_date_time =%s"
    cursor.execute(query, (flight_number, airline_name, dep_date))
    data = cursor.fetchall()
    if (not data):
        error = "No flight founded, please check your flight information"
        return render_template('staff_home.html', username=username, error5=error)
    query = "UPDATE flight SET status = %s WHERE flight_number=%s and departure_date_time=%s and airline_name=%s"
    cursor.execute(query, (status, flight_number, dep_date, airline_name))
    cursor.close()
    return render_template("staff_home.html", success="Successful change status")


@app.route('/view_reports', methods=['GET', 'POST'])
def view_reports():
    username = session["username"]
    start_date = request.form["start_date"]
    end_date = request.form["end_date"]
    cursor = conn.cursor()
    query = 'SELECT * FROM staff WHERE username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    if (not data):
        error = "No authentication for this action"
        return render_template('staff_home.html', error6=error)
    # TODO: 每个月的!!!!


@app.route('/view_rating', methods=['GET', 'POST'])
def view_rating():
    error = Auth_staff()
    if (error != None):
        return render_template("staff_home.html", error7=error)
    flight_number = request.form['flight_number']
    airline_name = get_airline_name()
    dep_date = request.form["departure_date"]
    dep_date=dep_date.replace("T"," ")+":00"
    cursor = conn.cursor()
    query = 'SELECT avg(rating) FROM rate WHERE flight_number = %s and departure_date_time = %s and airline_name=%s'
    cursor.execute(query, (flight_number, airline_name, dep_date))
    avg = cursor.fetchone()[0]
    query = "SELECT rate, comment FROM rate WHERE flight_number = %s and departure_date_time = %s and airline_name=%s"
    cursor.execute(query, (flight_number, airline_name, dep_date))
    data = cursor.fetchall()
    return render_template("staff_home.html", average=avg, rating_comment=data)


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
    query = 'SELECT * FROM customer WHERE email = %s and password = %s'
    cursor.execute(query, (username, password))
    # stores the results in a variable
    data = cursor.fetchone()
    if (not data):
        isStaff = True
        query = 'SELECT * FROM staff WHERE username = %s and password = %s'
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
    query = 'SELECT * FROM user WHERE username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    error = "Error with the input"
    if (data):
        # If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register_staff.html', error=error)
    else:
        ins = 'INSERT INTO staff VALUES(%s, %s, %s, %s,%s, %s)'
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
        ins = 'INSERT INTO Customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (
            email, name, password, building_number, street, city, state, phone_number, passport_number,
            passport_expiration,
            passport_country, date_of_birth))
        conn.commit()
        cursor.close()
        return render_template('login.html')


# Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    # grabs information from the forms
    username = request.form['username']
    password = request.form['password']

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM user WHERE username = %s'
    cursor.execute(query, (username))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    error = None
    if (data):
        # If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register.html', error=error)
    else:
        ins = 'INSERT INTO user VALUES(%s, %s)'
        cursor.execute(ins, (username, password))
        conn.commit()
        cursor.close()
        return render_template('index.html')


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

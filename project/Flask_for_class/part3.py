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
    # TODO: check
    trip_type = request.form['trip_type']
    source_city = request.form['source_city']
    source_airport = request.form['source_airport']
    des_city = request.form['des_city']
    des_airport = request.form['des_airport']
    date = request.form["departure_date"]
    return_date = request.form["return_date"]
    cursor = conn.cursor()
    if trip_type == "round":
        query = "SELECT e.flight_number, date(e.departure_date_time) as departure_date, e.airline_name, f.flight_number" \
                " as return_flight_number, date(f.departure_date_time) as return_date, f.airline_name as return_airline_name " \
                "from(SELECT b.flight_number, b.departure_date_time, b.airline_name, arrival_date_time FROM Airport as a join " \
                "(select flight_number, departure_date_time, airline_name, depart_airport_code,arrival_date_time, arrive_airport_code " \
                "from Flight)as b on b.depart_airport_code=a.code join Airport as c on b.arrive_airport_code=c.code WHERE a.city= %s and" \
                "a.name=%s and c.city=%s and c.name=%s and date(b.departure_date) = %s)e inner join(SELECT b.flight_number, b.departure_date_time, " \
                "b.airline_name FROM Airport as a join (select flight_number, departure_date_time, airline_name, depart_airport_code, " \
                "arrive_airport_code from Flight)as b on b.depart_airport_code=a.code join Airport as c on b.arrive_airport_code=c.code " \
                "WHERE a.city= %s and a.name=%s and c.city=%s and c.name=%s and date(b.departure_date) = %s)f " \
                "on e.arrival_date_time < f.departure_date_time"
        cursor.execute(query, (source_city, source_airport, des_city, des_airport, date, source_city, source_airport, des_city, des_airport, return_date))
    else:
        query = 'SELECT b.flight_number, b.departure_date, b.airline_name, ''as return_flight_number, '' as return_date, ''as return_airline_name ' \
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
    # TODO: 格式不对
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
    return render_template('customer_home.html', username=username, future_flight=data1, flight_type = flight_type)


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
    # TODO:转换格式
    dep_date = request.form["departure_date"]
    name_on_card = request.form["name_on_card"]
    card_num = request.form["card_num"]
    expir_date = request.form["expiration_date"]
    cursor = conn.cursor()
    ##TODO: 怎么找到future
    query = "SELECT flight_number,departure_date_time,airline_name " \
            "FROM flight" \
            "WHERE flight_number=%s and airline_name = %s and departure_date_time =%s"
    cursor.execute(query, (flight_number, airline_name, dep_date))
    data = cursor.fetchall()
    if (not data):
        error = "Please check the flight information"
        return render_template('customer_home.html', username=username, error2=error)
    # TODO: 查找座位id，算座位和价钱的逻辑
    query = 'INSERT INTO buy VALUES(%s,%s,%s,%s,%s,%s,%s)'
    # TODO：当前时间的计算，通过python或者sql
    # TODO: cursor.execute(query, (ticket_id,username,now,name_on_card,card_num,card_type,expir_date))
    data1 = cursor.fetchall()
    cursor.close()
    return render_template('customer_home.html', username=username, error="Successful buy tickets")


@app.route('/comment_and_rate', methods=['GET', 'POST'])
def comment_and_rate():
    username = session['username']
    flight_number = request.form["flight_number"]
    airline_name = request.form["airline_name"]
    # TODO:转换格式
    dep_date = request.form["departure_date"]
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
    return render_template('customer_home.html', username=username, error3="Successful rate and commented")


@app.route('/staff_home')
def staff_home():
    username = session['username']
    cursor = conn.cursor()
    # TODO: 接下来30天的
    query = "SELECT flight_number,departure_date_time,airline_name " \
            "FROM staff natural join airline natural join flight " \
            "WHERE username = %s ORDER BY departure_date_time DESC"
    cursor.execute(query, (username))
    data1 = cursor.fetchall()
    cursor.close()
    return render_template('staff_home.html', username=username, airline_fights=data1)


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
        return render_template("staff_home.html", error2="Successful added Airport")


@app.route('/create_new_airplane', methods=['GET', 'POST'])
def create_new_airplane():
    username = session["username"]
    airline_name = request.form['airline_name']
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
                return render_template("staff_home.html", error3="Successful added airplane")


@app.route('/find_customer', methods=['GET', 'POST'])
def find_customer():
    username = session["username"]
    flight_number = request.form['flight_number']
    airline_name = request.form['airline_name']
    dep_date = request.form["departure_date"]
    cursor = conn.cursor()
    query = 'SELECT * FROM staff WHERE username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    if (not data):
        error = "No authentication for this action"
        return render_template('staff_home.html', error1=error)
    query = "SELECT flight_number,departure_date_time,airline_name " \
            "FROM flight" \
            "WHERE flight_number=%s and airline_name = %s and departure_date_time =%s"
    cursor.execute(query, (flight_number, airline_name, dep_date))
    data = cursor.fetchall()
    if (not data):
        error = "Please check the flight information"
        return render_template('staff_home.html', username=username, error1=error)

    query = "SELECT name, phone_number" \
            "FROM customer natural join buy natural join ticket natural join flight" \
            "WHERE flight_number=%s and airline_name = %s and departure_date_time =%s"
    cursor.execute(query, (flight_number, airline_name, dep_date))
    data = cursor.fetchone()
    return render_template("staff_home.html", customers=data)


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
        # creates a session for the the user
        # session is a built in
        session['username'] = username
        if (isStaff):
            # TODO: homepage build for staff
            return redirect(url_for('staff_home'))
        else:
            # TODO: homepage build for customer
            return redirect(url_for('customer_home', if_initial = 1))
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


@app.route('/home')
def home():
    username = session['username']
    cursor = conn.cursor();
    query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    cursor.execute(query, (username))
    data1 = cursor.fetchall()
    for each in data1:
        print(each['blog_post'])
    cursor.close()
    return render_template('home.html', username=username, posts=data1)


"""
@app.route('/post', methods=['GET', 'POST'])
def post():
    username = session['username']
    cursor = conn.cursor();
    blog = request.form['blog']
    query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
    cursor.execute(query, (blog, username))
    conn.commit()
    cursor.close()
    return redirect(url_for('home'))
"""


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

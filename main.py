from flask import Flask, render_template, redirect, request, url_for
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
# configure the database
app.config['MYSQL_DATABASE_USER'] = 'ov80cru0603nr2bt'
app.config['MYSQL_DATABASE_PASSWORD'] = 'qxdso61zt25wr6bp'
app.config['MYSQL_DATABASE_DB'] = 'p3cnghzr0by5j7qg'
app.config['MYSQL_DATABASE_HOST'] = 'ble5mmo2o5v9oouq.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
mysql.init_app(app)


# create home page route
@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/myaccount/')
def account():
    return render_template('myaccount.html')

@app.route('/mytrips/')
def trips():
    return render_template('mytrips.html')

@app.route('/editgroup/', methods=['GET', 'POST'])
def editGroup():
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT group_name FROM travel_group")
    groups = cursor.fetchall()
    groups = [row[0] for row in groups]

    return render_template('editgroup.html', groups = groups)

@app.route('/addmember/', methods=['GET', 'POST'])
def addmember():
    conn = mysql.connect()
    cursor = conn.cursor()

    group_name = request.args['group']

    cursor.close()
    conn.close()


    return render_template('addmember.html', group_name = group_name)

@app.route('/removemember', methods=['GET', 'POST'])
def removemember():
    conn = mysql.connect()
    cursor = conn.cursor()

    group_name = request.args['group']

    sql = f'CALL view_group_members("{group_name}")'
    cursor.execute(sql)
    members = cursor.fetchall()
    members = [row[1] for row in members]


    cursor.close()
    conn.close()

    return render_template('removemember.html', group_name = group_name, members = members)

@app.route('/removesuccess', methods=['GET', 'POST'])
def removesuccess():
    conn = mysql.connect()
    cursor = conn.cursor()

    group_name = request.args['group_name']
    member_name = request.args['member_name']
    dob = request.args['dob']

    sql = f'CALL remove_member_from_group("{member_name}", "{dob}", "{group_name}")'
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()

    return render_template('removesuccess.html')

@app.route('/creategroup/', methods=['GET', 'POST'])
def createGroup():
    return render_template('creategroup.html')

@app.route('/addsuccess', methods=['GET', 'POST'])
def addMember():
    conn = mysql.connect()
    cursor = conn.cursor()

    group_name = request.args['group_name']
    member_name = request.args['member_name']
    dob = request.args['dob']
    email = request.args['email']
    sql = f'CALL create_group("{group_name}")'
    cursor.execute(sql)
    conn.commit()

    sql = f'CALL add_member("{member_name}", "{dob}", "{email}")'

    cursor.execute(sql)
    conn.commit()

    sql = f'CALL add_member_to_group("{member_name}", "{dob}", "{group_name}")'
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()
    return render_template('addsuccess.html')

@app.route('/viewagroup', methods=['GET', 'SET'])
def viewagroup():
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "SELECT group_name FROM travel_group"
    cursor.execute(sql)
    results = cursor.fetchall()
    results = [row[0] for row in results]

    cursor.close()
    conn.close()
    return render_template("viewagroup.html", results=results)

@app.route('/group')
def group():
    conn = mysql.connect()
    cursor = conn.cursor()

    group_name = request.args['group']

    sql3 = f'CALL view_group_members("{group_name}")'
    cursor.execute(sql3)
    member_headers = [i[0] for i in cursor.description]
    members = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("group.html", headers=member_headers, members=members
                        ,name=group_name)


@app.route('/viewgroups')
def viewGroups():
    conn = mysql.connect()
    cursor = conn.cursor()

    # this is an example showing how you would get the results from a query into a formatted table
    sql1 = "CALL view_groups()"
    cursor.execute(sql1)
    headers = [i[0] for i in cursor.description]
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('viewGroups.html', results=results, headers=headers)


@app.route('/deletegroupsuccess')
def deletegroupsuccess():
    conn = mysql.connect()
    cursor = conn.cursor()
    group_name = request.args['group']
    sql = f'CALL delete_group("{group_name}")'
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()
    return render_template('deletegroupsuccess.html', group = group_name)
@app.route('/createtrip/', methods=['POST', 'GET'])
def createTrip():
    conn = mysql.connect()
    cursor = conn.cursor()
    # change this to instead allow you to create a random new trip and travel_group
    '''
    going to want to add a new page that allows you to select a restaurant or hotel or excursion and add that to a
    trip number.... would suggest doing this using two drop downs ... ie restaurant name and trip_id and then using
    your stored procedure to insert those into the database
    '''


    # # do the SQL here to get all the different options we want into a list
    cursor.execute("SELECT group_name FROM travel_group")
    groups = cursor.fetchall()
    groups = [row[0] for row in groups]

    cursor.execute("SELECT name FROM excursion")
    excursions = cursor.fetchall()
    excursions = [row[0] for row in excursions]
    #
    cursor.execute("SELECT name FROM hotel")
    hotels = cursor.fetchall()
    hotels = [row[0] for row in hotels]
    #
    cursor.execute("SELECT name FROM restaurant")
    restaurants = cursor.fetchall()
    restaurants = [row[0] for row in restaurants]

    cursor.close()
    conn.close()
    return render_template("createtrip.html", excursions=excursions, restaurants=restaurants,
                        hotels=hotels, travel_groups = groups)

@app.route('/success', methods=['GET', 'POST'])
def submitSuccess():
    conn = mysql.connect()
    cursor = conn.cursor()
    # this will get the user selections

    hotel = request.args['hotel']
    restaurant = request.args['restaurant']
    excursion = request.args['excursion']
    trip_name = request.args['trip_name']
    group_name = request.args['group_name']
    start_date = request.args['start_date']
    end_date = request.args['end_date']
    sql = f"CALL create_trip('{group_name}', '{trip_name}', '{start_date}', '{end_date}')"
    cursor.execute(sql)

    # do sql here to actually insert it into the database
    cursor.execute( 'CALL add_hotel("' + hotel + '", "' + trip_name + '")')
    cursor.execute( 'CALL add_restaurant("' + restaurant + '", "' + trip_name + '")')
    cursor.execute( 'CALL add_excursion("' + excursion + '", "' + trip_name + '")')
    conn.commit()
    cursor.close()
    conn.close()
    return render_template("success.html")

@app.route('/edittrip/')
def editTrip():
    # put the SQL here to collect information from users about what they want to update
    # going to need another form to do this
    return render_template("editTrip.html")

@app.route('/deletetrip', methods=['GET', 'POST'])
def deletetrip():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = f'SELECT name FROM trip'
    cursor.execute(sql)
    trips = cursor.fetchall()
    trips = [row[0] for row in trips]

    cursor.close()
    conn.close()
    return render_template('deletetrip.html', trips = trips)

@app.route('/deletetripsuccess')
def deletetripsuccess():
    conn = mysql.connect()
    cursor = conn.cursor()
    trip_name = request.args['trip_name']
    sql = f'CALL delete_trip("{trip_name}")'
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()
    return render_template('deletetripsuccess.html', trip = trip_name)

@app.route('/edithotels', methods = ['GET', 'POST'])
def edithotels():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT name FROM trip"
    cursor.execute(sql)
    results = cursor.fetchall()
    results = [row[0] for row in results]

    cursor.close()
    conn.close()

    return render_template('edithotels.html', results = results)

@app.route('/addhotel', methods=['GET', 'POST'])
def addhotel():
    conn = mysql.connect()
    cursor = conn.cursor()
    trip_name = request.args['trip']

    cursor.execute("SELECT name FROM hotel")
    hotels = cursor.fetchall()
    hotels = [row[0] for row in hotels]

    cursor.close()
    conn.close()
    return render_template('addhotel.html', trip = trip_name, hotels = hotels)

@app.route('/addhotel/addhotelsuccess')
def addhotelsuccess():
    conn = mysql.connect()
    cursor = conn.cursor()

    trip_name = request.args['trip_name']
    hotel = request.args['hotel']
    sql = f'CALL add_hotel("{hotel}", "{trip_name}")'
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()
    return render_template('addhotelsuccess.html')

@app.route('/removehotel/', methods=['GET', 'POST'])
def removehotel():
    conn = mysql.connect()
    cursor = conn.cursor()
    trip_name = request.args['trip']
    sql = f'''SELECT name FROM hotel WHERE name in (SELECT h.name FROM trip_has_hotel
            JOIN hotel h USING (hotel_id) WHERE trip_id = (SELECT trip_id FROM trip WHERE name
            = "{trip_name}"))
            '''
    cursor.execute(sql)
    hotels = cursor.fetchall()
    hotels = [row[0] for row in hotels]

    cursor.close()
    conn.close()
    return render_template('removehotel.html', hotels = hotels, trip = trip_name)

@app.route('/removehotel/removehotelsuccess')
def removehotelsuccess():
    conn = mysql.connect()
    cursor = conn.cursor()
    trip_name = request.args['trip_name']
    hotel = request.args['hotel']

    sql = f'CALL remove_hotel("{hotel}", "{trip_name}")'
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()
    return render_template('removehotelsuccess.html')
@app.route('/editrestaurants', methods=['GET', 'POST'])
def editrestaurants():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT name FROM trip"
    cursor.execute(sql)
    results = cursor.fetchall()
    results = [row[0] for row in results]

    cursor.close()
    conn.close()
    return render_template('editrestaurants.html', results=results)

@app.route('/addrestaurant', methods = ['GET', 'POST'])
def addrestaurant():
    conn = mysql.connect()
    cursor = conn.cursor()
    trip_name = request.args['trip']

    cursor.execute("SELECT name FROM restaurant")
    restaurants = cursor.fetchall()
    restaurants = [row[0] for row in restaurants]

    cursor.close()
    conn.close()

    return render_template('addrestaurant.html', trip = trip_name, restaurants = restaurants)

@app.route('/addresaurant/addrestaurantsuccess')
def addrestaurantsuccess():
    conn = mysql.connect()
    cursor = conn.cursor()

    trip_name = request.args['trip_name']
    restaurant = request.args['restaurant']
    sql = f'CALL add_restaurant("{restaurant}", "{trip_name}")'
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()

    return render_template('addrestaurantsuccess.html')

@app.route('/removerestaurant', methods=['GET', 'SET'])
def removerestaurant():
    conn = mysql.connect()
    cursor = conn.cursor()
    trip_name = request.args['trip']
    sql = f'''SELECT name FROM restaurant WHERE name in (SELECT h.name FROM trip_has_restaurant
                JOIN restaurant h USING (restaurant_id) WHERE trip_id = (SELECT trip_id FROM trip WHERE name
                = "{trip_name}"))
                '''
    cursor.execute(sql)
    restaurants = cursor.fetchall()
    restaurants = [row[0] for row in restaurants]

    cursor.close()
    conn.close()
    return render_template('removerestaurant.html', restaurants=restaurants, trip=trip_name)

@app.route('/removerestaurant/removerestaurantsuccess')
def removerestaurantsuccess():
    conn = mysql.connect()
    cursor = conn.cursor()
    trip_name = request.args['trip_name']
    restaurant = request.args['restaurant']

    sql = f'CALL remove_restaurant("{restaurant}", "{trip_name}")'
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()
    return render_template('removerestaurantsuccess.html')

@app.route('/addexcursion', methods = ['GET', 'POST'])
def addexcursion():
    conn = mysql.connect()
    cursor = conn.cursor()
    trip_name = request.args['trip']

    cursor.execute("SELECT name FROM excursion")
    excursions = cursor.fetchall()
    excursions = [row[0] for row in excursions]

    cursor.close()
    conn.close()

    return render_template('addexcursion.html', trip = trip_name, excursions = excursions)

@app.route('/addexcursion/addexcursionsuccess')
def addexcursionsuccess():
    conn = mysql.connect()
    cursor = conn.cursor()

    trip_name = request.args['trip_name']
    excursion = request.args['excursion']
    sql = f'CALL add_excursion("{excursion}", "{trip_name}")'
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()

    return render_template('addexcursionsuccess.html')

@app.route('/removeexcursion', methods=['GET', 'SET'])
def removeexcursion():
    conn = mysql.connect()
    cursor = conn.cursor()
    trip_name = request.args['trip']
    sql = f'''SELECT name FROM excursion WHERE name in (SELECT h.name FROM trip_has_excursion
                JOIN excursion h USING (excursion_id) WHERE trip_id = (SELECT trip_id FROM trip WHERE name
                = "{trip_name}"))
                '''
    cursor.execute(sql)
    excursions = cursor.fetchall()
    excursions = [row[0] for row in excursions]

    cursor.close()
    conn.close()
    return render_template('removeexcursion.html', excursions = excursions, trip=trip_name)

@app.route('/removeexcursion/removeexcursionsuccess')
def removeexcursionsuccess():
    conn = mysql.connect()
    cursor = conn.cursor()
    trip_name = request.args['trip_name']
    excursion = request.args['excursion']

    sql = f'CALL remove_excursion("{excursion}", "{trip_name}")'
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()
    return render_template('removeexcursionsuccess.html')

@app.route('/editexcursions', methods=['GET', 'POST'])
def editexcursions():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT name FROM trip"
    cursor.execute(sql)
    results = cursor.fetchall()
    results = [row[0] for row in results]

    cursor.close()
    conn.close()
    return render_template('editexcursions.html', results=results)


@app.route('/tripSuccess/')
def tripSuccess():
    conn = mysql.connect()
    cursor = conn.cursor()
    THING = request.args['THING']
    THING1 = request.args['THING1']
    try:
        sql = "UPDATE trips SET THING = %s WHERE THING1= %s;" %(THING, THING1)
        cursor.execute(sql)
        conn.commit()
    except:
        print("An error has occured")
    cursor.close()
    conn.close()

    return render_template("success.html")

@app.route('/viewTrip/')
def viewTrip():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT name FROM trip"
    cursor.execute(sql)
    results = cursor.fetchall()
    results = [row[0] for row in results]
    cursor.close()
    conn.close()
    return render_template("viewTrips.html", results=results)

@app.route('/viewTrip/trip/')
def trip():
    conn = mysql.connect()
    cursor = conn.cursor()

    trip_name = request.args['trip']

    # finds the trip excursions
    sql = f'CALL view_trip_excursions("{trip_name}")'
    cursor.execute(sql)
    excursionHeaders = [i[0] for i in cursor.description]
    tripExcursions = cursor.fetchall()

    # finds the trip hotels
    sql2 = f'CALL view_trip_hotels("{trip_name}")'
    cursor.execute(sql2)
    hotelHeaders = [i[0] for i in cursor.description]
    tripHotels = cursor.fetchall()

    # finds the trip restaurants
    sql3 = f'CALL view_trip_restaurants("{trip_name}")'
    cursor.execute(sql3)
    restaurantHeaders = [i[0] for i in cursor.description]
    tripRestaurants = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template("trip.html", excursionHeaders=excursionHeaders, tripExcursions=tripExcursions,
                           hotelHeaders=hotelHeaders, tripHotels=tripHotels, restaurantHeaders=restaurantHeaders,
                           tripRestaurants=tripRestaurants, name=trip_name)


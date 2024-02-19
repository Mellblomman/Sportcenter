import psycopg2

#Update price
def update_price(activity, new_price):
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="____DITT LÖSENORD HÄR_____",
        post="5432"
    )
    cursor = conn.cursor()

    query = f"UPDATE court SET price = {new_price} WHERE activity = {activity}"

    cursor.execute(query)
    conn.commit()

    conn.close()

#Availability
def toggle_availability(activity):
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="____DITT LÖSENORD HÄR_____",
        post="5432"
    )
    cursor = conn.cursor()

    query = f"UPDATE court SET availability = CASE WHEN availability = TRUE THEN FALSE ELSE TRUE END WHERE activity = {activity}"

    cursor.execute(query)
    conn.commit()

    conn.close()

#Add activity
def add_activity(new_activity, new_datetime, new_price, new_availability):
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="____DITT LÖSENORD HÄR_____",
        post="5432"
    )
    cursor = conn.cursor()

    query = f"INSERT INTO court (court_id, activity, datetime, price, availability) VALUES ({new_activity}, {new_datetime}, {new_price}, {new_availability})"

    cursor.execute(query)
    conn.commit()

    conn.close()

#Delete activity
def delete_activity(activity):
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="____DITT LÖSENORD HÄR_____",
        post="5432"
    )
    cursor = conn.cursor()

    query = f"DELETE FROM court WHERE activity = {activity}"

    cursor.execute(query)
    conn.commit()

    conn.close()

#Update time of booking
def update_booking_time(booking_id, new_datetime):
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="____DITT LÖSENORD HÄR_____",
        post="5432"
    )
    cursor = conn.cursor()

    query = f"UPDATE bookings SET datetime = '{new_datetime}' WHERE booking_id = {booking_id}"

    cursor.execute(query)
    conn.commit()

    conn.close()

#Cancel booking
def cancel_booking(booking_id):
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="____DITT LÖSENORD HÄR_____",
        post="5432"
    )
    cursor = conn.cursor()

    query = f"DELETE FROM bookings WHERE booking_id = {booking_id}"
    
    cursor.execute(query)
    conn.commit()

    conn.close()

def get_filtered_bookings(email):
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="____DITT LÖSENORD HÄR_____",
        post="5432"
    )
    
    cursor = conn.cursor()

    query = f"SELECT bookinginformation.booking_id, bookinginformation.activity, bookinginformation.datetime, bookinginformation.email, bookinginformation.phone
        FROM bookinginformation
        JOIN court ON bookinginformation.activity = court.activity
        WHERE bookinginformation.email = {email};"
    
    cursor.execute(query)
    conn.commit()

    conn.close()


def get_available_time_slots():
    activity = request.args.get('activity')

    if not activity:
        return jsonify({"error": "Activity parameter is required"}), 400

    # Read database credentials from the JSON file
    credentials = read_credentials('path/to/credentials.json')

    # Define the SELECT query with parameterized query
    query = """
        SELECT datetime FROM court
        WHERE activity = %s AND availability = TRUE
        ORDER BY datetime;
    """

    # Execute the query and return the results as JSON
    results = execute_query(query, (activity,), credentials)
    
    # Extracting datetime values from the result
    time_slots = [result[0] for result in results]

    return jsonify({"available_time_slots": time_slots})
import psycopg2

#Update price
def update_price(activity, new_price):
    conn = psycopg2.connect(
        host="postgres",
        user="postgres",
        database="postgres"
    )
    cursor = conn.cursor()

    query = f"UPDATE court SET price = {new_price} WHERE activity = {activity}"

    cursor.execute(query)
    conn.commit()

    conn.close()

#Availability
def toggle_availability(activity):
    conn = psycopg2.connect(
        host="postgres",
        user="postgres",
        database="postgres"
    )
    cursor = conn.cursor()

    query = f"UPDATE court SET availability = CASE WHEN availability = TRUE THEN FALSE ELSE TRUE END WHERE activity = {activity}"

    cursor.execute(query)
    conn.commit()

    conn.close()

#Add activity
def add_activity(new_activity, new_datetime, new_price, new_availability):
    conn = psycopg2.connect(
        host="postgres",
        user="postgres",
        database="postgres"
    )
    cursor = conn.cursor()

    query = f"INSERT INTO court (court_id, activity, datetime, price, availability) VALUES ({new_activity}, {new_datetime}, {new_price}, {new_availability})"

    cursor.execute(query)
    conn.commit()

    conn.close()

#Delete activity
def delete_activity(activity):
    conn = psycopg2.connect(
        host="postgres",
        user="postgres",
        database="postgres"
    )
    cursor = conn.cursor()

    query = f"DELETE FROM court WHERE activity = {activity}"

    cursor.execute(query)
    conn.commit()

    conn.close()

#Update time of booking
def update_booking_time(booking_id, new_datetime):
    conn = psycopg2.connect(
        host="postgres",
        user="postgres",
        database="postgres"
    )
    cursor = conn.cursor()

    query = f"UPDATE bookings SET datetime = '{new_datetime}' WHERE booking_id = {booking_id}"

    cursor.execute(query)
    conn.commit()

    conn.close()

#Cancel booking
def cancel_booking(booking_id):
    conn = psycopg2.connect(
        host="postgres",
        user="postgres",
        database="postgres"
    )
    cursor = conn.cursor()

    query = f"DELETE FROM bookings WHERE booking_id = {booking_id}"
    
    cursor.execute(query)
    conn.commit()

    conn.close()

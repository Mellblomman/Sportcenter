import psycopg2

#Update price
def update_price(court_id, new_price):
    conn = psycopg2.connect(
        host='your_postgres_host',
        user='your_postgres_user',
        password='your_postgres_password',
        database='your_database'
    )
    cursor = conn.cursor()

    query = f"UPDATE court SET price = {new_price} WHERE court_id = {court_id}"

    cursor.execute(query)
    conn.commit()

    conn.close()

#Availability
def toggle_availability(court_id):
    conn = psycopg2.connect(
        host='your_postgres_host',
        user='your_postgres_user',
        password='your_postgres_password',
        database='your_database'
    )
    cursor = conn.cursor()

    query = f"UPDATE court SET availability = CASE WHEN availability = TRUE THEN FALSE ELSE TRUE END WHERE court_id = {court_id}"

    cursor.execute(query)
    conn.commit()

    conn.close()

#Add activity
def add_activity(new_court_id, new_activity, new_datetime, new_price, new_availability):
    conn = psycopg2.connect(
        host='your_postgres_host',
        user='your_postgres_user',
        password='your_postgres_password',
        database='your_database'
    )
    cursor = conn.cursor()

    query = f"INSERT INTO court (court_id, activity, datetime, price, availability) VALUES ({new_court_id}, {new_activity}, {new_datetime}, {new_price}, {new_availability})"

    cursor.execute(query)
    conn.commit()

    conn.close()

#Delete activity
def delete_activity(court_id):
    conn = psycopg2.connect(
        host='your_postgres_host',
        user='your_postgres_user',
        password='your_postgres_password',
        database='your_database'
    )
    cursor = conn.cursor()

    query = f"DELETE FROM court WHERE court_id = {court_id}"

    cursor.execute(query)
    conn.commit()

    conn.close()

#Update time of booking
def update_booking_time(booking_id, new_datetime):
    conn = psycopg2.connect(
        host='your_postgres_host',
        user='your_postgres_user',
        password='your_postgres_password',
        database='your_database'
    )
    cursor = conn.cursor()

    query = f"UPDATE bookings SET datetime = '{new_datetime}' WHERE booking_id = {booking_id}"

    cursor.execute(query)
    conn.commit()

    conn.close()

#Cancel booking
def cancel_booking(booking_id):
    conn = psycopg2.connect(
        host='your_postgres_host',
        user='your_postgres_user',
        password='your_postgres_password',
        database='your_datebase'
    )
    cursor = conn.cursor()

    query = f"DELETE FROM bookings WHERE booking_id = {booking_id}"
    
    cursor.execute(query)
    conn.commit()

    conn.close()

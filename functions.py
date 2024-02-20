import psycopg2, random

conn_details = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "megaine11",
    "port": '5432'
} 

def fetch_user_bookings_from_database(email):
    try:
        conn = psycopg2.connect(**conn_details)
        cur = conn.cursor()
        cur.execute("SELECT * FROM user_bookings_view WHERE email = %s", (email,))
        user_bookings = cur.fetchall()
        cur.close()
        conn.close()
        return user_bookings
    except psycopg2.Error as e:
        print("Error fetching user bookings:", e)
        return None
    
def booking_confirmed(activity, date, time, email, phone):
    try:
        conn = psycopg2.connect(**conn_details)
        cur = conn.cursor()

        while True:
            random_number = random.randint(000000, 999999)

            # Kontrollera om det slumpmässiga numret redan finns i databasen
            cur.execute("SELECT * FROM bookinginformation WHERE booking_id = %s", (random_number,))
            result = cur.fetchone()

            if result:
                print(f"{random_number} finns i databasen.")
            else:
                print(f"{random_number} finns inte i databasen.")
                break

        # Sätt in bokningsinformationen i databasen med det slumpmässiga boknings-id
        cur.execute("INSERT INTO bookinginformation (booking_id, activity, date, time, email, phone) VALUES (%s, %s, %s, %s, %s, %s)",
                    (random_number, activity, date, time, email, phone))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except psycopg2.Error as e:
        print("Error inserting booking information:", e)
        return False
    
def delete_booking_from_database(booking_id): # Funktion som kollar om booking_id finns i databasen och raderar
    try: # Anslutning till databas
        conn = psycopg2.connect(**conn_details) # **conn_details i Python betyder att du "expanderar" dictionaryn conn_details till nyckel-värde-par
        cur = conn.cursor() #  Verktyg för att interagera med databaser från Python-kod.
        cur.execute("DELETE FROM bookinginformation WHERE booking_id = %s", (booking_id,)) # utför en operation men inget är permanent. conn.commit() gör det permanent.
        conn.commit() # används för att "bekräfta" alla ändringar som gjorts under den aktuella transaktionen, DVS raderingen av booking_id i databasen
        rows_deleted = cur.rowcount # Kontrollera antalet rader som påverkades av raderingen
        cur.close() # Stänger cursor eftersom vi inte behöver den mer, frigör resurser.
        conn.close() # Stänger anslutningen till postgreSQL
        
        if rows_deleted > 0:
            return True  # Returnera True om minst en rad togs bort (dvs bokningen fanns)
        else:
            return False
    except psycopg2.Error as e:
        print("Error deleting booking:", e) # Vid anslutningsfel eller felaktig syntax i sql-fråga.
        return False

def fetch_activities_from_database():
    try:
        conn = psycopg2.connect(**conn_details)
        cur = conn.cursor()
        cur.execute("SELECT TRIM(BOTH ',' FROM activity) FROM court")
        activities = [row[0] for row in cur.fetchall()]  # Extrahera aktiviteterna från tuples
        cur.close()
        conn.close()
        return activities
    except psycopg2.Error as e:
        print("Error fetching activities:", e)
        return None

def admin_or_not(email):
    try:
        conn = psycopg2.connect(**conn_details)
        cur = conn.cursor()
        cur.execute("SELECT admin FROM inloggningsuppgifter WHERE email = %s", (email,))
        admin_status = cur.fetchone()[0]
        cur.close()
        conn.close()
        return admin_status
    except psycopg2.Error as e:
        return None

def login_credentials_check(email, password):
    try:
        conn = psycopg2.connect(**conn_details)
        cur = conn.cursor()
        cur.execute("SELECT password, email, admin FROM inloggningsuppgifter WHERE email = %s AND password = %s", (email, password,))
        user_info = cur.fetchall()
        cur.close()
        conn.close()
        if user_info:
            print(user_info)  # Kontrollera om användaren finns i databasen
            return True
        print(user_info)
        return False
    except psycopg2.Error as e:
        print("Error checking login credentials:", e)
        return False

def admin_change_price(activity, price):
    try:
        conn = psycopg2.connect(**conn_details)
        cur = conn.cursor()
        cur.execute("UPDATE court SET price = %s WHERE activity = %s", (price, activity))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except psycopg2.Error as e:
        print("Error checking login credentials:", e)
        return False

def admin_delete_activity(activity):
    try:
        conn = psycopg2.connect(**conn_details)
        cur = conn.cursor()
        cur.execute("DELETE FROM court WHERE activity = %s", (activity,))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except psycopg2.Error as e:
        print("Error checking login credentials:", e)
        return False         

def admin_add_activity(activity, price):
    try:
        conn = psycopg2.connect(**conn_details)
        cur = conn.cursor()
        cur.execute("INSERT INTO court (activity, price) VALUES (%s, %s)",
                    (activity, price,))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except psycopg2.Error as e:
        print("Error checking login credentials:", e)
        return False               
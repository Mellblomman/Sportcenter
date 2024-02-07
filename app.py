from flask import Flask, request, render_template, url_for, session, redirect
import os
import psycopg2
from datetime import datetime
import random

app = Flask(__name__)

app.secret_key = os.urandom(24)

@app.route("/", methods=["GET"])
def render_index():
    return render_template("index.html")

@app.route("/contact.html", methods=["GET"])
def render_contact():
    return render_template("contact.html")

@app.route("/cancellation.html", methods=["GET"])
def render_cancellation():
    return render_template("cancellation.html")

@app.route("/confirmationcontact.html", methods=["POST"])
def render_confirmationcontact():
    return render_template("confirmationcontact.html", message="<span style='color: white;'>Tack för ditt mail, vi återkommer inom kort.</span>")

@app.route("/boka.html", methods=["GET"])
def render_padelbooking():
    return render_template("boka.html")

conn_details = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "Mydatabase1391",
    "port": '5432'
}

@app.route("/confirmationcancellation.html", methods=["POST"])
def delete_booking():
    booking_id = request.form.get("booking_id") # Sparar datan användaren skriver in på hemsidan i booking_id variabeln
    if booking_id:
        if delete_booking_from_database(booking_id):
            return render_template("confirmationcancellation.html", message="Avbokat")
        else:
            return render_template("confirmationcancellation.html", message="Hittade ingen bokning med det id")
    else:
        return render_template("confirmationcancellation.html", message="Inget bokningsid angivet")
            
       
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
    
@app.route("/bookingconfirmed.html", methods=["POST"])
def de_booking():
    activity = request.form.get("activity")
    datetime = request.form.get("datetime")
    email = request.form.get("email")
    phone = request.form.get("phone")
    input_data = (activity, datetime, email, phone)
    
    if input_data:
        if booking_confirmed(activity, datetime, email, phone):
            conn = psycopg2.connect(**conn_details)
            cur = conn.cursor()
            cur.execute("SELECT booking_id, datetime FROM bookinginformation WHERE email = %s", (email,))
            booking_info = cur.fetchone()
            cur.close()
            conn.close()
            if booking_info:
                booking_id = booking_info[0]
                booking_datetime = booking_info[1]
                return render_template("bookingconfirmed.html", message="Bokningsinformationen har lagts till.", booking_id=booking_id, booking_datetime=booking_datetime)
            else:
                return render_template("bookingconfirmed.html", message="Ingen bokning hittades med den angivna e-postadressen.")
        else:
            return render_template("bookingconfirmed.html", message="Det gick inte att lägga till bokningsinformationen.")
    else:
        return render_template("bookingconfirmed.html", message="Nödvändiga uppgifter saknas.")  # Vi når aldrig denna???


def booking_confirmed(activity, datetime, email, phone):
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
        cur.execute("INSERT INTO bookinginformation (booking_id, activity, datetime, email, phone) VALUES (%s, %s, %s, %s, %s)",
                    (random_number, activity, datetime, email, phone))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except psycopg2.Error as e:
        print("Error inserting booking information:", e)
        return False
    
























if __name__ == "__main__":
    app.run(debug=True)




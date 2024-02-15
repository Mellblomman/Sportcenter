from flask import Flask, request, render_template, url_for, session, redirect
import os
import re
import psycopg2
from datetime import datetime
import random

app = Flask(__name__)

app.secret_key = os.urandom(24)

@app.route("/", methods=["GET"])
def render_index():
    return render_template("index.html")



@app.route("/inloggning.html", methods=["POST"])
def render_inloggning():
    return render_template("inloggning.html")


@app.route("/inloggad.html", methods=["POST", "GET"])
def render_inloggad():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email and password: 
            if login_credentials_check(email, password):
                return render_template("inloggad.html", message="Välkommen", email=email)
            else:
                return render_template("inloggning.html", message="Felaktiga inloggningsuppgifter. Var god försök igen eller skapa ett nytt konto")
        else:
            return render_template("inloggning.html")
    else:
        # Om det inte är en POST-förfrågan, returnera bara inloggningssidan
        return render_template("inloggning.html")

def login_credentials_check(email, password):
    try:
        conn = psycopg2.connect(**conn_details)
        cur = conn.cursor()
        cur.execute("SELECT password, email FROM inloggningsuppgifter WHERE email = %s AND password = %s", (email, password,))
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



@app.route("/bookings.html", methods=["POST", "GET"])
def render_bookings():
    return render_template("bookings.html")

@app.route("/registration.html", methods=["POST", "GET"])
def render_registration():
    return render_template("registration.html")

@app.route("/registrationstatus.html", methods=["POST", "GET"])
def render_registrationstatus():
    return render_template("registrationstatus.html")


@app.route("/contact.html", methods=["GET"])
def render_contact():
    return render_template("contact.html")

@app.route("/cancellation.html", methods=["GET"])
def render_cancellation():
    return render_template("cancellation.html")

@app.route("/confirmationcontact.html", methods=["POST"])
def render_confirmationcontact():
    if request.method == "POST":
        # Kontrollera om filen meddelande.txt finns, annars skapas den
        if not os.path.isfile("meddelanden.txt"):
            with open("meddelanden.txt", "w", encoding="utf-8"):
                pass  # Skapar filen om den inte finns

        # Regex-mönster för att validera e-postadress
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        # Regex-mönster för att validera telefonnummer (exakt 10 siffror)
        phone_pattern = r"^\d{10}$"
        # Regex-mönster för att validera meddelandet (minst 3 tecken)
        message_pattern = r"^(?=\s*\S)(.{3,}(?:\s+\S+){0,299}\s*)$"

        # Validera e-postadress
        if not re.match(email_pattern, request.form["email"]):
            return render_template("/confirmationcontact.html", message="<span style='color: white;'>Felaktig e-postadress!</span>")

        # Validera telefonnummer
        if not re.match(phone_pattern, request.form["telefon"]):
            return render_template("/confirmationcontact.html", message="<span style='color: white;'>Felaktigt telefonnummer, fyll i 10 siffror!</span>")

        # Validera meddelandet
        if not re.match(message_pattern, request.form["message"]):
            return render_template("/confirmationcontact.html", message="<span style='color: white;'>Meddelandet måste vara minst 3 tecken långt!</span>")

        # Om allt är korrekt, spara datan
        with open("meddelanden.txt", "a", encoding="utf-8") as file:
            file.write(f"{request.form['email']}, {request.form['telefon']}, {request.form['message']}\n")
        return render_template("/confirmationcontact.html", message="<span style='color: white;'>Tack för ditt mail, vi återkommer inom kort.</span>")
    else:
        return "Metoden är inte tillåten"


@app.route("/boka.html", methods=["GET"])
def render_padelbooking():
    return render_template("boka.html")

conn_details = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "megaine11",
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
    
def booking_confirmed(booking_id, activity, datetime, email, phone):
    try:
        conn = psycopg2.connect(**conn_details)
        cur = conn.cursor()

        # Ta bort den befintliga bokningen baserat på det angivna bokningsnumret
        cur.execute("DELETE FROM bookinginformation WHERE booking_id = %s", (booking_id,))
        conn.commit()

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
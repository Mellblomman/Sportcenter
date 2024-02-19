from flask import Flask, request, render_template, url_for, session, redirect, jsonify
import os
import re
import psycopg2
from datetime import datetime
import random

app = Flask(__name__)

app.secret_key = os.urandom(24)

@app.route("/", methods=["GET", "POST"])
def render_index():
    return render_template("index.html")

@app.route("/adminpage.html", methods=["POST", "GET", "PUT"])
def render_adminpage():
    activity = request.form.get("activity")
    price = request.form.get("price")
    datetime = request.form.get("datetime")
    
    if 'add_activity' in request.form:
        if 'Lägg till en aktivitet' in request.form.values():
            if admin_add_activity(activity, price, datetime):
                return render_template("adminpage.html", message="Aktivitet tillagd")
            else:
                return render_template("adminpage.html", message="Något gick fel med att lägga till aktivitet")
              
    elif 'Ta bort aktivitet' in request.form.values():
        if admin_delete_activity(activity):
            return render_template("adminpage.html", message="Aktivitet raderad")
        else:
            return render_template("adminpage.html", message="Något gick fel med att radera aktiviteten")
    elif 'Nytt pris' in request.form.values():
        if admin_change_price(activity, price):
            return render_template("adminpage.html", message="Priset uppdaterat")
        else:
            return render_template("adminpage.html", message="Något gick fel med att uppdatera priset")

    return render_template("adminpage.html", message="Välkommen Admin")

def admin_add_activity(activity, price, datetime):
    try:
        conn = psycopg2.connect(**conn_details)
        cur = conn.cursor()
        cur.execute("INSERT INTO court (activity, price, datetime) VALUES (%s, %s, %s)",
                    (activity, price, datetime,))
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



@app.route("/inloggning.html", methods=["POST"])
def render_inloggning():
    return render_template("inloggning.html")


@app.route("/inloggad.html", methods=["POST", "GET"])
def render_inloggad():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        session["email"] = email

        if email and password: 
            if login_credentials_check(email, password):
                admin_status = admin_or_not(email)
                if admin_status:
                    return redirect(url_for('render_adminpage'))
                else:
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

@app.route("/activities.html", methods=["GET"])
def render_activities():
    activities = fetch_activities_from_database()
    if activities:
        return render_template("activities.html", activities=activities)
    else:
        return render_template("activities.html", message="Inga aktiviteter hittades.")

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

@app.route("/registration.html", methods=["POST", "GET"])
def render_registration():
    return render_template("registration.html")

@app.route("/contact.html", methods=["GET"])
def render_contact():
    return render_template("contact.html")

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

conn_details = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "megaine11",
    "port": '5432'
}          
       
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
    
@app.route("/logincancellation.html", methods=["GET"])
def render_logincancellation():
    return render_template("logincancellation.html")

@app.route("/loginboka.html", methods=["GET"])
def render_loginboka():
    return render_template("loginboka.html")

@app.route("/logincontact.html", methods=["GET"])
def render_logincontact():
    return render_template("logincontact.html")

@app.route("/loginindex.html", methods=["GET"])
def render_loginindex():
    return render_template("loginindex.html")

@app.route("/loginconfirmationcancellation.html", methods=["POST","GET"])
def delete_login_booking():
    booking_id = request.form.get("booking_id") # Sparar datan användaren skriver in på hemsidan i booking_id variabeln
    if booking_id:
        if delete_booking_from_database(booking_id):
            return render_template("loginconfirmationcancellation.html", message="Avbokat")
        else:
            return render_template("loginconfirmationcancellation.html", message="Hittade ingen bokning med det id")
    else:
        return render_template("loginconfirmationcancellation.html", message="Inget bokningsid angivet")

@app.route("/loginconfirmationcontact.html", methods=["POST", "GET"])
def render_login_confirmationcontact():
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
            return render_template("/loginconfirmationcontact.html", message="<span style='color: white;'>Felaktig e-postadress!</span>")

        # Validera telefonnummer
        if not re.match(phone_pattern, request.form["telefon"]):
            return render_template("/loginconfirmationcontact.html", message="<span style='color: white;'>Felaktigt telefonnummer, fyll i 10 siffror!</span>")

        # Validera meddelandet
        if not re.match(message_pattern, request.form["message"]):
            return render_template("/loginconfirmationcontact.html", message="<span style='color: white;'>Meddelandet måste vara minst 3 tecken långt!</span>")

        # Om allt är korrekt, spara datan
        with open("meddelanden.txt", "a", encoding="utf-8") as file:
            file.write(f"{request.form['email']}, {request.form['telefon']}, {request.form['message']}\n")
        return render_template("/loginconfirmationcontact.html", message="<span style='color: white;'>Tack för ditt mail, vi återkommer inom kort.</span>")
    else:
        return "Metoden är inte tillåten"
    
@app.route("/loginbookingconfirmed.html", methods=["POST", "GET"])
def de_login_booking():
    activity = request.form.get("activity")
    date  = request.form.get("date")
    time = request.form.get("time")
    email = request.form.get("email")
    phone = request.form.get("phone")
    input_data = (activity, date, time, email, phone)

    # Regex-mönster för att validera e-postadress
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    # Regex-mönster för att validera telefonnummer (exakt 10 siffror)
    phone_pattern = r"^\d{10}$"
    

    # Validera e-postadress
    if not re.match(email_pattern, request.form["email"]):
        return render_template("/loginboka.html", message="<span style='color: white;'>Felaktig e-postadress!</span>")

    # Validera telefonnummer
    if not re.match(phone_pattern, request.form["phone"]):
        return render_template("/loginboka.html", message="<span style='color: white;'>Felaktigt telefonnummer, fyll i 10 siffror!</span>")
    
    if input_data:
        conn = psycopg2.connect(**conn_details)
        cur = conn.cursor()
        cur.execute("SELECT * FROM bookinginformation WHERE activity = %s AND date = %s AND time = %s", (activity, date, time,))
        available_time = cur.fetchone()
        if available_time == None:
            pass
        else:
            return redirect(url_for("render_loginbookingfail"))
    
    if input_data:
        if booking_confirmed(activity, date, time, email, phone):
            conn = psycopg2.connect(**conn_details)
            cur = conn.cursor()
            cur.execute("SELECT booking_id, date, time FROM bookinginformation WHERE email = %s AND date = %s AND time = %s", (email, date, time,))
            booking_info = cur.fetchone()
            cur.close()
            conn.close()
            if booking_info:
                booking_id = booking_info[0]
                booking_datetime = booking_info[1]
                return render_template("loginbookingconfirmed.html", message="Bokningsinformationen har lagts till.", booking_id=booking_id, booking_datetime=booking_datetime)
            else:
                return render_template("loginbookingconfirmed.html", message="Ingen bokning hittades med den angivna e-postadressen.")
        else:
            return render_template("loginbookingconfirmed.html", message="Det gick inte att lägga till bokningsinformationen.")
    else:
        return render_template("loginbookingconfirmed.html", message="Nödvändiga uppgifter saknas.")  # Vi når aldrig denna???    

@app.route("/loginbookingfail.html", methods=["POST", "GET"])
def render_loginbookingfail():
    return render_template("loginbookingfail.html")

@app.route("/registrationstatus.html", methods=["GET", "POST"])
def register_user_status():
    email = request.form.get("email")
    password = request.form.get("password")
    phone = request.form.get("phone")
    input_data = (email, password, phone)

    # Regex-mönster för att validera e-postadress
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    # Regex-mönster för att validera password (minst 5 tecken)
    password_pattern = r"^(?=\s*\S)(.{5,}(?:\s+\S+){0,30}\s*)$"
    # Regex-mönster för att validera telefonnummer (exakt 10 siffror)
    phone_pattern = r"^\d{10}$"
    

    # Validera e-postadress
    if not re.match(email_pattern, request.form["email"]):
        return render_template("/registration.html", message="<span style='color: white;'>Felaktig e-postadress!</span>")

    # Validera telefonnummer
    if not re.match(phone_pattern, request.form["phone"]):
        return render_template("/registration.html", message="<span style='color: white;'>Felaktigt telefonnummer, fyll i 10 siffror!</span>")

    # Validera meddelandet
    if not re.match(password_pattern, request.form["password"]):
        return render_template("/registration.html", message="<span style='color: white;'>Lösenordet behöver vara minst 5 tecken långt!</span>")

    if input_data:
        try:
            conn = psycopg2.connect(**conn_details)
            cur = conn.cursor()
            cur.execute("INSERT INTO inloggningsuppgifter (email, password, phone) VALUES (%s, %s, %s)",
                        (email, password, phone))
            conn.commit()
            cur.close()
            conn.close()
            return render_template("registrationstatus.html", message="Konto skapat, var god logga in")
        except psycopg2.Error as e:
            print("Error inserting user information:", e)
            return render_template("registrationstatus.html", message="Ett fel uppstod vid registreringen. Vänligen försök igen senare.")
    else:
        return render_template("registrationstatus.html", message="Nödvändiga uppgifter saknas")



@app.route("/bookings.html", methods=["GET", "POST"])
def get_user_bookings():
    # Här kan du använda sessionsinformationen eller någon form av autentisering för att identifiera den aktuella användaren
    # Antag att användarens e-postadress är lagrad i sessionsvariabeln 'email'

    if "email" in session:  # Förutsatt att du har lagrat användarens e-postadress i sessionsvariabeln 'email'
        email = session["email"]
        user_bookings = fetch_user_bookings_from_database(email)
        if user_bookings is not None:
            return render_template("bookings.html", bookings=user_bookings)
        else:
            return render_template("bookings.html", message="Inga bokningar hittades för den aktuella användaren.")
    else:
        return jsonify({"error": "Användaren är inte inloggad"}), 401  # 401 Unauthorized om användaren inte är inloggad


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
    


if __name__ == "__main__":
    app.run(debug=True)   
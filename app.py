from flask import Flask, request, render_template, url_for
import os
import calendar
import psycopg2
from datetime import datetime
app = Flask(__name__)

@app.route("/", methods=["GET"])
def render_index():
    return render_template("index.html")

@app.route("/contact.html", methods=["GET"])
def render_contact():
    return render_template("contact.html")

@app.route("/activities.html", methods=["GET"])
def render_activities():
    return render_template("activities.html")

@app.route("/cancellation.html", methods=["GET"])
def render_cancellation():
    return render_template("cancellation.html")

#@app.route("/confirmationcancellation.html", methods=['POST'])
#def confirmationcancellation():
#    return render_template("confirmationcancellation.html", message="<span style='color: white;'>Tack för din avbokning, vi hoppas att vi syns inom snar framtid!</span>")


@app.route("/badminton.html", methods=["GET"])
def render_badminton():
    return render_template("badminton.html", message="<span style='color: white;'>Badminton</span>")

@app.route("/football.html", methods=["GET"])
def render_football():
    return render_template("football.html", message="<span style='color: white;'>Fotboll</span>")

@app.route("/gymnastics.html", methods=["GET"])
def render_gymnastics():
    return render_template("gymnastics.html", message="<span style='color: white;'>Gymnastik</span>")



@app.route("/tennis.html", methods=["GET"])
def render_tennis():
    return render_template("tennis.html", message="<span style='color: white;'>Tennis</span>")

@app.route("/confirmationcontact.html", methods=["POST"])
def render_confirmationcontact():
    return render_template("confirmationcontact.html", message="<span style='color: white;'>Tack för ditt mail, vi återkommer inom kort.</span>")

def generate_calendar(year, month):
    cal = calendar.HTMLCalendar(calendar.SUNDAY)
    # Generate the HTML for the calendar
    cal_html = cal.formatmonth(year, month)
    # Add attributes to each day to make them clickable
    cal_html = cal_html.replace('<td ', '<td class="calendar-day" data-year="{0}" data-month="{1}" '.format(year, month))
    return cal_html

@app.route("/padel.html", methods=["GET"])
def render_padel():
    now = datetime.now()
    year = now.year
    month = now.month
    cal_html = generate_calendar(year, month)
    return render_template("padel.html", calendar=cal_html, message="<span style='color: white;'>Padel</span>")

@app.route("/padelbooking.html", methods=["POST"])
def render_padelbooking():
    return render_template("padelbooking.html")

@app.route("/padelbookingconfirmed.html", methods=["POST"])
def render_padelbookingconfirmed():
    return render_template("padelbookingconfirmed.html")




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
    if booking_id: # Om användaren matar in någon data.
        if delete_booking_from_database(booking_id):
            return render_template("confirmationcancellation.html", message="Avbokat")
        else:
            return render_template("confirmationcancellation.html", message="hittade inget a")
            
       
def delete_booking_from_database(booking_id): # Funktion som kollar om booking_id finns i databasen och raderar
    try: # Anslutning till databas
        conn = psycopg2.connect(**conn_details) # **conn_details i Python betyder att du "expanderar" dictionaryn conn_details till nyckel-värde-par
        cur = conn.cursor() #  Verktyg för att interagera med databaser från Python-kod.
        cur.execute("DELETE FROM bookings WHERE booking_id = %s", (booking_id,)) # utför en operation men inget är permanent. conn.commit() gör det permanent.
        conn.commit() # används för att "bekräfta" alla ändringar som gjorts under den aktuella transaktionen, DVS raderingen av booking_id i databasen
        cur.close() # Stänger cursor eftersom vi inte behöver den mer, frigör resurser.
        conn.close() # Stänger anslutningen till postgreSQL
        return True 
    except psycopg2.Error as e:
        print("Error deleting booking:", e) # Vid anslutningsfel eller felaktig syntax i sql-fråga.
        return False
    

























if __name__ == "__main__":
    app.run(debug=True)




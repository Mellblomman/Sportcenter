from flask import Flask, request, render_template, url_for
import os
import calendar
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

@app.route("/confirmationcancellation.html", methods=['POST'])
def confirmationcancellation():
    return render_template("confirmationcancellation.html", message="<span style='color: white;'>Tack för din avbokning, vi hoppas att vi syns inom snar framtid!</span>")


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


if __name__ == "__main__":
    app.run(debug=True)




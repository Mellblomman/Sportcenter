Devops Sportcenter
En app som företag kan använda för att deras kunder ska kunna boka deras banor för vald sport.

Inledning
Devops Sportcenter är utformad för att göra det enkelt för företag att erbjuda deras kunder en applikation
där kunden på ett smidigt och enkelt sätt kan boka deras banor.

Installation
1. Hämta gitrepot:
https://github.com/Mellblomman/Sportcenter.git

2. Installera en venv genom att skriva följande i terminalen
py -m venv venv
om det inte fungerar skriv
py3 -m venv venv

3. Installera packages i din virtual environment
pip install flask
pip install psycopg2

4. Skapa en lokal databas
Ladda ner extension SQLTools och SQLTools PostgreSQL/Cockroach Driver
OBS viktigt att ändra lösenordet till ditt lösenord i conn_details 
längst upp i functions.py
Exempel:
conn_details = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "ÄNDRA LÖSENORDET",
    "port": '5432'
} 

5. Navigera till databas.sql
Kör följande tables:
CREATE TABLE court (
    activity VARCHAR(10) PRIMARY KEY,
    price int
);

CREATE TABLE bookinginformation (
    booking_id INT NOT NULL,
    activity VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    PRIMARY KEY(activity, date, time)
);

CREATE TABLE inloggningsuppgifter (
    email VARCHAR(255) PRIMARY KEY,
    password VARCHAR(30),
    phone VARCHAR(10),
    admin boolean DEFAULT 'FALSE'
);

CREATE VIEW user_bookings_view AS
    SELECT bi.*, c.price
    FROM bookinginformation bi
    JOIN court c ON bi.activity = c.activity;

Tryck CTRL+E två gånger för att skapa tabellerna och viewn.

6. Kör följande querys i databasen
-- Skapa admin konto
INSERT INTO inloggningsuppgifter(email, PASSWORD, phone, ADMIN)VALUES
('admin','admin','0000000000', TRUE);

-- Viktiga inserts
Insert INTO court(activity, price) VALUES
('Tennis','200');

Insert INTO court(activity, price) VALUES
('Handboll','200');

7. Kör applikationen
source venv/scripts/activate
flask run

-- Viktiga tables
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

-- Skapa admin konto
INSERT INTO inloggningsuppgifter(email, PASSWORD, phone, ADMIN)VALUES
('--','--','--', TRUE);

-- Viktiga inserts
Insert INTO court(activity, price) VALUES
('Tennis','200');

Insert INTO court(activity, price) VALUES
('Handboll','200');



-- Dropa alla tables
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;




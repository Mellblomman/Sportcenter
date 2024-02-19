-- Här kan man lagra ban information
CREATE TABLE court (
    activity VARCHAR(10) PRIMARY KEY,
    price int
);
INSERT INTO court VALUES('Padel', 250);
DROP TABLE bookinginformation CASCADE;

-- Här sparas ens personuppgifter
CREATE TABLE bookinginformation (
    booking_id INT NOT NULL,
    activity VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    PRIMARY KEY(activity, date, time)
);

INSERT INTO bookinginformation (booking_id, activity, date, time, email, phone)VALUES (12345, 'Tennis', '2024-03-03', '12:00', 'test@gmail.com', '0707929323');
DROP TABLE bookinginformation CASCADE;

CREATE TABLE inloggningsuppgifter (
    email VARCHAR(255),
    password VARCHAR(30),
    phone VARCHAR(10),
    admin boolean DEFAULT 'FALSE'
);

UPDATE court
SET price = 100
WHERE activity ='testsport';
DROP TABLE inloggningsuppgifter;
INSERT INTO inloggningsuppgifter VALUES ('hej@gmail.com', 'abc123', '0000000000');

-- Får ut datum tid utan sekunder och minuter
SELECT TO_CHAR(datetime, 'YYYY-MM-DD HH24') AS formatted_timestamp
FROM court;

-- Test
INSERT INTO court(activity, price, datetime, availability)VALUES
('Fotboll', 150, '2024-01-12 20:35:20', TRUE);

INSERT INTO bookinginformation(booking_id, activity, datetime, email, phone)VALUES
('3', 'Tennis', '2024-01-12 20:35:20', 'mattias@outlook.com','073123456');

INSERT INTO inloggningsuppgifter(email, PASSWORD, phone, ADMIN)VALUES
('mattias@outlook.com','Test123','073123456', FALSE);

DELETE FROM bookinginformation WHERE booking_id = 3;

CREATE SCHEMA public;
DROP SCHEMA public CASCADE;

CREATE VIEW user_bookings_view AS
    SELECT bi.*, c.price
    FROM bookinginformation bi
    JOIN court c ON bi.activity = c.activity;

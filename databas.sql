-- Här kan man lagra ban information
CREATE TABLE court (
    activity VARCHAR(10) PRIMARY KEY,
    price int,
    datetime TIMESTAMP,
    availability BOOLEAN NOT NULL
);

-- Här sparas ens personuppgifter
CREATE TABLE bookinginformation (
    booking_id INT,
    activity VARCHAR(10), 
    datetime TIMESTAMP,
    email VARCHAR(255),
    phone VARCHAR(20),
    PRIMARY KEY(booking_id, datetime)
);

CREATE TABLE inloggningsuppgifter (
    email VARCHAR(255),
    password VARCHAR(30),
    phone VARCHAR(10),
    admin boolean DEFAULT 'FALSE'
);

DROP TABLE inloggningsuppgifter;
INSERT INTO inloggningsuppgifter VALUES ('hej@gmail.com', 'abc123', '0000000000');

-- Får ut datum tid utan sekunder och minuter
SELECT TO_CHAR(datetime, 'YYYY-MM-DD HH24') AS formatted_timestamp
FROM court;

-- Test
INSERT INTO court(activity, price, datetime, availability)VALUES
('Tennis', 150, '2024-01-12 20:35:20', TRUE);

INSERT INTO bookinginformation(booking_id, activity, datetime, email, phone)VALUES
('3', 'Tennis', '2024-01-12 20:35:20', 'mattias@outlook.com','073123456');

INSERT INTO inloggningsuppgifter(email, PASSWORD, phone, ADMIN)VALUES
('mattias@outlook.com','Test123','073123456', FALSE);

DELETE FROM bookinginformation WHERE booking_id = 3;

CREATE SCHEMA public;
DROP SCHEMA public CASCADE;

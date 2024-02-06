-- Här kan man lagra ban information
CREATE TABLE court (
    court_id VARCHAR(10) PRIMARY KEY,
    activity VARCHAR(30),
    price int,
    datetime TIMESTAMP,
    availability BOOLEAN NOT NULL
);

-- Bookningar
CREATE TABLE bookings (
    booking_id INT PRIMARY KEY,
    court_id VARCHAR(10), 
    datetime TIMESTAMP,
    FOREIGN KEY (court_id) REFERENCES court(court_id)
);

-- Här sparas ens personuppgifter
CREATE TABLE bookinginformation (
    booking_id INT,
    email VARCHAR(255),
    phone VARCHAR(20),
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE CASCADE
);

-- Får ut datum tid utan sekunder och minuter
SELECT TO_CHAR(datetime, 'YYYY-MM-DD HH24') AS formatted_timestamp
FROM court;

-- Test
INSERT INTO court(court_id, activity, price, datetime, availability)VALUES
('12346','Tennis', 150, '2024-01-12 20:35:20',TRUE);

INSERT INTO bookings (booking_id, court_id, datetime)VALUES
('3','12346','2024-01-12 20:35:20');

INSERT INTO bookinginformation(booking_id, email, phone)VALUES
('3','mattias@outlook.com','073123456');

DELETE FROM bookings WHERE booking_id = 1;

CREATE SCHEMA public;
DROP SCHEMA public CASCADE;

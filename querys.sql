UPDATE court
SET price = new_price
WHERE court_id = your_court_id;


UPDATE court
SET availability = CASE WHEN availability = TRUE THEN FALSE ELSE TRUE END
WHERE court_id = your_court_id;


INSERT INTO court (court_id, activity, datetime, price, availability)
VALUES (your_court_id, 'New Activity', 'New DateTime', new_price, 'Available');


DELETE FROM court
WHERE court_id = your_court_id;


UPDATE bookings
SET datetime = new_datetime
WHERE booking_id = your_booking_id;

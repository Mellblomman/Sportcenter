UPDATE court
SET price = new_price
WHERE court_id = your_court_id;


UPDATE court
SET availability = CASE WHEN availability = TRUE THEN FALSE ELSE TRUE END
WHERE court_id = your_court_id;


INSERT INTO court (court_id, activity,  price, datetime, availability)
VALUES (new_court_id, new_activity, new_datetime, new_price, new_availability);


DELETE FROM court
WHERE court_id = your_court_id;


UPDATE bookings
SET datetime = new_datetime
WHERE booking_id = your_booking_id;

DELETE FROM bookings
WHERE booking_id = your_booking_id;

SELECT bookinginformation.booking_id, bookinginformation.activity, bookinginformation.datetime, bookinginformation.email, bookinginformation.phone
FROM bookinginformation
JOIN court ON bookinginformation.activity = court.activity
WHERE bookinginformation.email = 'example_email';
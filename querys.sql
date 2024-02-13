UPDATE court
SET price = new_price
WHERE activity = activity_name;


UPDATE court
SET availability = CASE WHEN availability = TRUE THEN FALSE ELSE TRUE END
WHERE activity = activity_name;


INSERT INTO court (activity,  price, datetime, availability)
VALUES (new_activity, new_datetime, new_price, new_availability);


DELETE FROM court
WHERE activity = activity_name;


UPDATE bookings
SET datetime = new_datetime
WHERE booking_id = your_booking_id;

DELETE FROM bookings
WHERE booking_id = your_booking_id;


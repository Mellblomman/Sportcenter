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

SELECT bookinginformation.booking_id, bookinginformation.activity, bookinginformation.datetime, bookinginformation.email, bookinginformation.phone
FROM bookinginformation
JOIN court ON bookinginformation.activity = court.activity
WHERE bookinginformation.email = 'example_email';

SELECT * FROM inloggningsuppgifter
WHERE email = 'user_email' AND password = 'user_password';

SELECT datetime FROM court
WHERE activity = %s AND availability = TRUE
ORDER BY datetime;

SELECT activity, datetime
FROM court
WHERE availability = true AND activity = 'your_specific_activity'
ORDER BY datetime;

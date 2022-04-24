-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description FROM crime_scene_reports
WHERE year = 2021 AND month = 7 AND day = 28 AND street = "Humphrey Street";

-- Theft took place at 10.15am at Humphrey Street Bakery.

SELECT transcript FROM interviews
WHERE year = 2021 AND month = 7 AND day = 28 AND transcript LIKE "%bakery%";

SELECT naem FROM people
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25
AND activity = "exit";

SELECT name FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street"
AND transaction_type = "withdraw";

SELECT name FROM people
JOIN passengers ON passangers.passport_number = people.passport_number
WHERE passengers.flight_id = (
    SELECT id FROM flights
    WHERE year = 2021 AND month = 7 AND day = 29 AND origin_airport_id = (
        SELECT id FROM airports WHERE city = "Fiftyville"
    )
    ORDER BY hour,minute
    LIMIT 1
);

SELECT name FROM people
JOIN phone_calls ON phone_calls.caller = people.phone_number
WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;

-- Finding the city the thief and accomplice escaped to.
SELECT city FROM airports
WHERE id = (
    SELECT destination_airport_id FROM flights
    WHERE year = 2021 AND month = 7 AND day = 29 AND origin_airport_id = (
        SELECT id FROM airports WHERE city = "Fiftyville")
        ORDER BY hour,minute
        LIMIT 1
    );

-- Finding the accomplice
SELECT phone_number FROM people WHERE name = "Bruce";
-- (367) 555-5533

SELECT name FROM people WHERE phone_number = (
    SELECT receiver FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28 ANd duration < 60 AND called = "(367) 555-5533"
);
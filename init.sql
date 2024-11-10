-- Switch to the new database (optional depending on PostgreSQL version)
\c sensordata;

-- Create the user if it doesn’t exist (optional, PostgreSQL may already use environment variables)
DO
$do$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'db_user') THEN
      CREATE ROLE db_user LOGIN PASSWORD 'S#cret123';
   END IF;
END
$do$;

-- Create the table for storing averaged sensor data
CREATE TABLE IF NOT EXISTS measurements (
    id SERIAL PRIMARY KEY,
    room_id INT,
    measurement_type VARCHAR(50),
    average_value DECIMAL(10, 2),
    unit VARCHAR(20),
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
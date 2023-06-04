\i schema_drop.sql

CREATE TABLE IF NOT EXISTS UFO_sightings (
    id SERIAL PRIMARY KEY,
    comments TEXT,
    latitude DECIMAL(11,8),
    longitude DECIMAL(11,8)
);

CREATE TABLE IF NOT EXISTS Users(
	username VARCHAR(30) PRIMARY KEY,
	password varchar(120),
);

CREATE TABLE IF NOT EXISTS Posts(
	post_number SERIAL PRIMARY KEY,
	longitude DECIMAL(11,8),
	latitude DECIMAL(11,8),
	comments TEXT,
	date_posted DATE,
	username VARCHAR(30) REFERENCES Users(username)
);

CREATE TABLE IF NOT EXISTS User_sightings (
    sighting_id SERIAL PRIMARY KEY,
	comments TEXT,
	latitude FLOAT,
	longitude FLOAT,
	username VARCHAR(30) REFERENCES users(username)
);

CREATE OR REPLACE FUNCTION add_to_ufo_sightings() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO UFO_sightings (comments, latitude, longitude) 
    VALUES (NEW.comments, NEW.latitude, NEW.longitude);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_ufo_sightings_trigger
AFTER INSERT ON Posts
FOR EACH ROW EXECUTE FUNCTION add_to_ufo_sightings();


-- CREATE VIEW IF NOT EXISTS Combined_sightings AS
-- SELECT comments, latitude, longitude
-- FROM UFO_sightings
-- UNION
-- SELECT comments, latitude, longitude
-- FROM User_sightings;

\i sql_ddl/vw_cd_sum.sql
\i sql_ddl/vw_invest_accounts.sql
\i sql_ddl/vw_invest_certificates.sql
\i sql_ddl/vw_tdw.sql

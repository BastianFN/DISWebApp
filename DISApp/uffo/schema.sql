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
	username VARCHAR(30) REFERENCES Users(username)
);

CREATE TABLE IF NOT EXISTS User_sightings (
    id SERIAL PRIMARY KEY,
    comments TEXT,
    latitude DECIMAL(11,8),
    longitude DECIMAL(11,8),
    username VARCHAR(30) REFERENCES Users(username)
);

CREATE VIEW IF NOT EXISTS Combined_sightings AS
SELECT id, city, state, country, comments, date_posted, latitude, longitude
FROM UFO_sightings
UNION
SELECT id, city, state, country, comments, date_posted, latitude, longitude
FROM User_sightings;

\i sql_ddl/vw_cd_sum.sql
\i sql_ddl/vw_invest_accounts.sql
\i sql_ddl/vw_invest_certificates.sql
\i sql_ddl/vw_tdw.sql

DROP TABLE IF EXISTS gears;


CREATE TABLE gears (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name varchar(255) NOT NULL,
  benefits varchar(255),
  drawbacks varchar(255),
  image TEXT,
  date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  user varchar(255) NOT NULL
);

INSERT INTO gears ({id}, {name}, {benefits}, {drawbacks},{image},{date},{user})

SELECT * FROM gears

UPDATE gears
SET id = {id}, name = {name}, benefits = {benefits}, drawbacks = {drawbacks}, image = {image}, date = {date}, user ={user}
WHERE id = {id}

delete from gears
WHERE id = {id}
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/wind_data.csv'
INTO TABLE wind_data
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES


CREATE TABLE IF NOT EXISTS weather_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(255),
    wind_degree INT,
    wind_kph FLOAT,
    precip_mm FLOAT,
    precip_in FLOAT,
    wind_direction VARCHAR(255),
    last_updated DATE,
    sunrise TIME
);

CREATE TABLE IF NOT EXISTS precip_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    precip_mm FLOAT,
    precip_in FLOAT,
    is_safe_to_go_out CHAR
);
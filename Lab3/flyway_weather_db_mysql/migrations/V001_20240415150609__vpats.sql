CREATE TABLE IF NOT EXISTS weather_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(255),
    wind_degree INT,
    wind_kph FLOAT,
    wind_mph FLOAT,
    wind_direction VARCHAR(255),
    last_updated DATE,
    sunrise TIME
);

CREATE TABLE IF NOT EXISTS wind_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    wind_speed_kph FLOAT,
    wind_speed_mph FLOAT,
    wind_direction VARCHAR(50),
    wind_degree INT,
    is_safe_to_go_out CHAR
);
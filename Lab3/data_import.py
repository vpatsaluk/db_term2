import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, WeatherData  # Переконайтеся, що моделі імпортовані правильно

engine = create_engine('postgresql://postgres:1805@localhost:5432/weather_db')
Session = sessionmaker(bind=engine)
session = Session()

def load_data(filepath):
    # Зчитування даних з CSV файлу
    data = pd.read_csv(filepath)
    return data


def insert_data(data):
    session = Session()
    for _, row in data.iterrows():
        weather_entry = WeatherData(
            country=row['country'],
            wind_degree=int(row['wind_degree']),
            wind_kph=float(row['wind_kph']),
            wind_mph=float(row['wind_mph']),
            wind_direction=row['wind_direction'],
            last_updated=pd.to_datetime(row['last_updated']).date(),
            sunrise=pd.to_datetime(row['sunrise']).time()
        )
        session.add(weather_entry)

    session.commit()


# Виклик функцій для завантаження та вставки даних
filepath = 'GlobalWeatherRepository.csv'
data = load_data(filepath)
insert_data(data)
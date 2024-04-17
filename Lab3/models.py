from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date, Time
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class WeatherData(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True)
    country = Column(String)
    wind_degree = Column(Integer)
    wind_kph = Column(Float)
    precip_mm = Column(Float)
    precip_in = Column(Float)
    wind_direction = Column(String)
    last_updated = Column(Date)
    sunrise = Column(Time)


engine = create_engine('postgresql://postgres:1805@localhost:5432/weather_db')
Base.metadata.create_all(engine)
from sqlalchemy import create_engine, select, Table, MetaData, Column, Integer, String, Float, Date, Time

engine = create_engine('postgresql://postgres:1805@localhost/weather_db')

metadata = MetaData()
weather_data = Table('weather_data', metadata,
    Column('id', Integer, primary_key=True),
    Column('country', String),
    Column('wind_degree', Integer),
    Column('wind_kph', Float),
    Column('precip_mm', Float),
    Column('precip_in', Float),
    Column('wind_direction', String),
    Column('last_updated', Date),
    Column('sunrise', Time),
)

def query_weather(country, date):
    with engine.connect() as connection:
        query = select(
            weather_data.columns.country,
            weather_data.columns.wind_degree,
            weather_data.columns.wind_kph,
            weather_data.columns.precip_mm,
            weather_data.columns.precip_in,
            weather_data.columns.wind_direction,
            weather_data.columns.last_updated,
            weather_data.columns.sunrise
        ).where(
            weather_data.columns.country == country,
            weather_data.columns.last_updated == date
        )

        result = connection.execute(query)
        for row in result:
            print(f"Country: {row[0]}, Wind Degree: {row[1]}, Wind KPH: {row[2]}, Precip mm: {row[3]}, "
                  f"Precip in {row[4]}, Wind Direction: {row[5]}, Last Updated: {row[6]}, Sunrise: {row[7]}")

country_input = input("Enter the country: ")
date_input = input("Enter the date (YYYY-MM-DD): ")

query_weather(country_input, date_input)

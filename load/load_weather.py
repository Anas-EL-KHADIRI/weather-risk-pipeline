    #type: ignore
def load_weather():
    import pandas as pd
    from sqlalchemy import select
    from sqlalchemy.orm import Session
    from load.database import engine
    from load.models import WeatherForecast,City
    from datetime import datetime
    import os

    
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

    weathers = pd.read_csv(f"{SCRIPT_DIR}/../gold/weather_gold.csv")

    with Session(engine) as session:
        for _, row in weathers.iterrows():

            city = session.scalar(
                select(City).where(City.city_name == row["city"])
            )

            if city is None:
                print(f"City not found: {row['city']}")
                continue

            forecast_date = pd.to_datetime(row["date"]).date()
            existing = session.query(WeatherForecast).filter_by(
                    city_id=city.id,
                    forecast_date=forecast_date
                ).first()

            if existing:
                print(row["city"], forecast_date, "→ already exists, skipped")
                continue
            forecast = WeatherForecast(
                forecast_date=forecast_date,
                temperature_max=row["temperature_max"],
                temperature_min=row["temperature_min"],
                precipitation=row["precipitation"],
                precipitation_probability=row["precipitation_probability"],
                wind_speed_max=row["wind_speed_max"],
                wind_gust_max=row["wind_gust_max"],
                weather_code=row["weather_code"],
                retrieved_at=datetime.now(),
                city_id=city.id
            )
            session.add(forecast)

            print(row["city"], "→", city.id)

        session.commit()
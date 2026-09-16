# type: ignore
def load_risks():
    import pandas as pd
    from sqlalchemy import select
    from sqlalchemy.orm import Session
    from load.database import engine
    from load.models import WeatherForecast, Risk, City
    import os

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

    weathers = pd.read_csv(
        f"{SCRIPT_DIR}/../gold/weather_gold.csv"
    )

    with Session(engine) as session:

        for _, row in weathers.iterrows():

            forecast_date = pd.to_datetime(row["date"]).date()

            forecast = session.scalar(
                select(WeatherForecast)
                .join(City)
                .where(
                    City.city_name == row["city"],
                    WeatherForecast.forecast_date == forecast_date
                )
            )

            if forecast is None:
                print(
                    f"Forecast not found: "
                    f"{row['city']} - {row['date']}"
                )
                continue

            risk = session.scalar(
                select(Risk)
                .where(
                    Risk.forecast_id == forecast.forecast_id
                )
            )

            if risk is None:

                risk = Risk(
                    forecast_id=forecast.forecast_id,
                    rain_risk=row["rain_risk"],
                    wind_risk=row["wind_risk"],
                    temperature_risk=row["temperature_risk"],
                    weather_code_risk=row["weather_code_risk"],
                    risk_score=row["risk_score"],
                    risk_level=row["risk_level"]
                )

                session.add(risk)

            else:

                risk.rain_risk = row["rain_risk"]
                risk.wind_risk = row["wind_risk"]
                risk.temperature_risk = row["temperature_risk"]
                risk.weather_code_risk = row["weather_code_risk"]
                risk.risk_score = row["risk_score"]
                risk.risk_level = row["risk_level"]

        session.commit()
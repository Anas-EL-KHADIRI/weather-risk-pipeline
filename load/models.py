from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    String,
    Integer,
    Float,
    ForeignKey,
    DateTime,
    Numeric,
    Date,
    UniqueConstraint,
    Column
)
from datetime import datetime, date


Base = declarative_base()


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True)
    city_name = Column(String(100), nullable=False)
    latitude = Column(Numeric(10, 6), nullable=False)
    longitude = Column(Numeric(10, 6), nullable=False)


class WeatherForecast(Base):
    __tablename__ = "weatherforecasts"

    __table_args__ = (
        UniqueConstraint(
            "city_id",
            "forecast_date",
            name="uq_city_forecast_date"
        ),
    )

    forecast_id = Column(Integer, primary_key=True)
    forecast_date = Column(Date, nullable=False)
    temperature_max = Column(Float, nullable=False)
    temperature_min = Column(Float, nullable=False)
    precipitation = Column(Float, nullable=False)
    precipitation_probability = Column(Float, nullable=False)
    wind_speed_max = Column(Float, nullable=False)
    wind_gust_max = Column(Float, nullable=False)
    weather_code = Column(Integer, nullable=False)
    retrieved_at = Column(DateTime, nullable=False)
    city_id = Column(
        Integer,
        ForeignKey("cities.id"),
        nullable=False
    )



class Risk(Base):
    __tablename__ = "risks"

    risk_id = Column(Integer, primary_key=True)

    forecast_id = Column(
        Integer,
        ForeignKey("weatherforecasts.forecast_id"),
        nullable=False,
        unique=True
    )

    rain_risk = Column(Float, nullable=False)
    wind_risk = Column(Float, nullable=False)
    temperature_risk = Column(Float, nullable=False)
    weather_code_risk = Column(Float, nullable=False)

    risk_score = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False)
#type: ignore
import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import engine
from models import City

cities = pd.read_csv("../extraction/ma.csv")
cities = cities[["city", "lat", "lng"]]

with Session(engine) as session:
    for _, row in cities.iterrows():
        city = City(
            city_name=row["city"],
            latitude=row["lat"],
            longitude=row["lng"]
        )

        session.add(city)

    session.commit()
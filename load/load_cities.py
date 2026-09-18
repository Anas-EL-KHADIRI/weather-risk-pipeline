#type: ignore
def load_cities():
    import pandas as pd
    from sqlalchemy import select
    from sqlalchemy.orm import Session
    from load.database import engine
    from load.models import City
    import os

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


    cities = pd.read_csv(f"{SCRIPT_DIR}/../extraction/ma.csv")
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
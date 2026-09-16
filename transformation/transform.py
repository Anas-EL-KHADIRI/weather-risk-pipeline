def transform():
    import json
    import pandas as pd # type: ignore
    import os
    
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    FILE_PATH = os.path.join(SCRIPT_DIR,"..","bronze","raw_data.json")
    with open(FILE_PATH, "r") as f:
        data = json.load(f)

    df = pd.json_normalize(data)

    df = df.rename(columns={
        "weather.daily.time": "date",
        "weather.daily.temperature_2m_max": "temperature_max",
        "weather.daily.temperature_2m_min": "temperature_min",
        "weather.daily.precipitation_sum": "precipitation",
        "weather.daily.precipitation_probability_max": "precipitation_probability",
        "weather.daily.wind_speed_10m_max": "wind_speed_max",
        "weather.daily.wind_gusts_10m_max": "wind_gust_max",
        "weather.daily.weather_code": "weather_code"
    })


    daily_columns = [
        "date",
        "temperature_max",
        "temperature_min",
        "precipitation",
        "precipitation_probability",
        "wind_speed_max",
        "wind_gust_max",
        "weather_code"
    ]
    df = df.explode(daily_columns,ignore_index=True)

    df = df[
        [
            "city",
            "lat",
            "lng",
            "date",
            "temperature_max",
            "temperature_min",
            "precipitation",
            "precipitation_probability",
            "wind_speed_max",
            "wind_gust_max",
            "weather_code"
        ]
    ]


    print(df.head())
    df["date"] = pd.to_datetime(df["date"])
    numeric_columns = [
        "lat",
        "lng",
        "temperature_max",
        "temperature_min",
        "precipitation",
        "precipitation_probability",
        "wind_speed_max",
        "wind_gust_max",
        "weather_code"
    ]

    df[numeric_columns] = df[numeric_columns].apply(
        pd.to_numeric,
        errors="coerce"
    )

    missing_values = df.isna().sum().sum()
    duplicates = df.duplicated().sum()
    city_date_duplicates = df.duplicated(subset=["city", "date"]).sum()

    invalid_precipitation = (df["precipitation"] < 0).sum()
    invalid_probability = (
        (df["precipitation_probability"] < 0) |
        (df["precipitation_probability"] > 100)
    ).sum()

    invalid_temperature = (
        df["temperature_max"] < df["temperature_min"]
    ).sum()

    if (
        missing_values == 0
        and duplicates == 0
        and city_date_duplicates == 0
        and invalid_precipitation == 0
        and invalid_probability == 0
        and invalid_temperature == 0
    ):
        print("data quality checks passed")
        df.to_csv(f"{SCRIPT_DIR}/../silver/weather_clean.csv", index=False)
        print("silver data exported")
    else:
        print("data quality checks failed\nsilver data was NOT exported")

    print(df.dtypes)
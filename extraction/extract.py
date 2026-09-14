import pandas as pd #type: ignore
import requests #type: ignore
import json

url = "https://api.open-meteo.com/v1/forecast"

cities = pd.read_csv("ma.csv")
cities=cities[["city","lat","lng"]]


raw_data=[]
failed_cities = []

for index, city in cities.iterrows():
    print(city["city"])
    params = {
    "latitude": city["lat"],
    "longitude": city["lng"],
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,wind_gusts_10m_max,weather_code",
    "forecast_days": 7
    }

    try:
        response = requests.get(url, params=params,timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error for {city['city']}: {e}")
        failed_cities.append(city["city"])
        continue

    print(response.status_code)

    try:
        data=response.json()
    except requests.exceptions.JSONDecodeError as e:
            print(f"Error : {e}")
            continue

    

    raw_data.append({
    "city": city["city"],
    "lat": city["lat"],
    "lng": city["lng"],
    "weather": data
    })



with open(f"../bronze/raw_data.json", "w") as file:
    json.dump(raw_data, file, indent=4)


if not failed_cities:
    print("all cities are fetched")
else:
    print("Failed cities:", failed_cities)
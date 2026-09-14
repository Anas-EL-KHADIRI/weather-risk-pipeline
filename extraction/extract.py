import pandas as pd #type: ignore
import requests #type: ignore


cities = pd.read_csv("ma.csv")
cities=cities[["city","lat","lng"]]
cities=cities.head(3)


city = cities.iloc[0]

print(city["city"])
print(city["lat"])
print(city["lng"])

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": city["lat"],
    "longitude": city["lng"],
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,wind_gusts_10m_max,weather_code",
    "forecast_days": 7
}

response = requests.get(url, params=params)

print(response.status_code)
data=response.json()
print(data["daily"])
import pandas as pd#type: ignore
df = pd.read_csv("../silver/weather_clean.csv")

def precipitation_category(precipitation):
    if precipitation == 0:
        return "none"
    elif precipitation <= 2:
        return "low"
    elif precipitation <= 10:
        return "moderate"
    elif precipitation <= 20:
        return "high"
    else:
        return "extreme"


df["precipitation_category"] = df["precipitation"].apply(
    precipitation_category
)


def temperature_category(temp):
    if temp < 10:
        return "Cold"
    elif temp <= 30:
        return "Normal"
    elif temp <= 35:
        return "Hot"
    else:
        return "Extreme"

df["temp_category"] = df["temperature_max"].apply(
    temperature_category
)



def wind_category(wind):
    if wind < 30:
        return "low"
    elif wind <= 50:
        return "moderate"
    elif wind <= 70:
        return "high"
    else:
        return "extreme"


df["wind_category"] = df["wind_speed_max"].apply(wind_category)


def precipitation_risk(precipitation):
    if precipitation == 0:
        return 0
    elif precipitation <= 2:
        return 20
    elif precipitation <= 10:
        return 40
    elif precipitation <= 20:
        return 70
    else:
        return 100


df["precipitation_risk"] = df["precipitation"].apply(precipitation_risk)


df["rain_risk"] = (
    df["precipitation_risk"]
    * df["precipitation_probability"]
    / 100
).round(2)


def wind_risk(wind, gust):
    if wind > 70 or gust > 90:
        return 100
    elif wind > 50 or gust > 70:
        return 70
    elif wind >= 30 or gust >= 50:
        return 40
    else:
        return 0


df["wind_risk"] = df.apply(
    lambda row: wind_risk(
        row["wind_speed_max"],
        row["wind_gust_max"]
    ),
    axis=1
)

def temperature_risk(temp):
    if 15 <= temp <= 30:
        return 0
    elif 10 <= temp < 15 or 30 < temp <= 35:
        return 30
    elif 5 <= temp < 10 or 35 < temp <= 40:
        return 60
    else:
        return 100


df["temperature_risk"] = df["temperature_max"].apply(
    temperature_risk
)

# print(df.loc[df["city"] == "Taroudannt", ["temperature_max", "temperature_risk"]])


def weather_code_risk(code):
    if code in [0, 1]:
        return 5

    elif code in [2, 3, 5, 6, 7, 8, 9, 10, 11, 12,
                  20, 21, 22, 23, 24, 28, 51, 61, 71, 80]:
        return 20

    elif code in [13, 14, 15, 16, 25, 26, 27, 45, 48,
                  53, 55, 63, 73, 81]:
        return 40

    elif code in [17, 18, 30, 31, 32, 33, 34, 35, 56, 57,
                  65, 66, 67, 75, 77, 82, 85, 86, 95, 96]:
        return 65

    elif code in [19, 36, 37, 38, 39, 97, 98, 99]:
        return 90

    else:
        return 0

df["weather_code_risk"] = df["weather_code"].apply(
    weather_code_risk
)


df["risk_score"] = (
    df["rain_risk"] * 0.40
    + df["wind_risk"] * 0.30
    + df["temperature_risk"] * 0.15
    + df["weather_code_risk"] * 0.15
).round(2)

def risk_level(score):
    if score < 25:
        return "Low"
    elif score < 50:
        return "Moderate"
    elif score < 75:
        return "High"
    else:
        return "Extreme"


df["risk_level"] = df["risk_score"].apply(risk_level)


# Gold data quality checks

missing_risk = df[
    ["rain_risk", "wind_risk", "temperature_risk",
     "weather_code_risk", "risk_score", "risk_level"]
].isna().sum().sum()

invalid_risk_score = (
    (df["risk_score"] < 0) |
    (df["risk_score"] > 100)
).sum()

duplicates = df.duplicated(
    subset=["city", "date"]
).sum()

valid_categories = (
    df["precipitation_category"].isin(
        ["none", "low", "moderate", "high", "extreme"]
    ).all()
    and
    df["temp_category"].isin(
        ["Cold", "Normal", "Hot", "Extreme"]
    ).all()
    and
    df["wind_category"].isin(
        ["low", "moderate", "high", "extreme"]
    ).all()
)

if (
    missing_risk == 0
    and invalid_risk_score == 0
    and duplicates == 0
    and valid_categories
):
    print("Gold data quality checks passed.")

    df.to_csv("../gold/weather_gold.csv", index=False)

    print("Gold data exported.")
else:
    print("Gold data quality checks failed.")
    print("Gold data was NOT exported.")
import streamlit as st
from sqlalchemy import text
from load.database import engine
import pandas as pd

st.set_page_config(
    page_title="Weather risk dashboard",
    page_icon="🌦️",
    layout="wide"
)

st.title("🌦️ Weather Risk Dashboard")

with engine.connect() as connection:
    result = connection.execute(
        text("SELECT COUNT(*) FROM cities")
    )

    number_of_cities = result.scalar()


with engine.connect() as connection:
    result = connection.execute(
        text("SELECT MAX(temperature_max) AS max_temperature FROM weatherforecasts")
    )

    max_temp = result.scalar()

with engine.connect() as connection:
    result = connection.execute(
        text("SELECT MIN(temperature_min) AS min_temperature FROM weatherforecasts")
    )

    min_temp = result.scalar()


with engine.connect() as connection:
    result = connection.execute(
        text("SELECT MAX(precipitation) AS max_precipitation FROM weatherforecasts")
    )

    max_precipitation = result.scalar()


with engine.connect() as connection:
    result = connection.execute(
        text("SELECT ROUND(AVG(risk_score)::numeric, 2) FROM risks")
    )

    avg_risk = result.scalar()

col1, col2, col3, col4 ,col5= st.columns(5)

col1.metric("Number of cities", number_of_cities)
col2.metric("Max temperature", max_temp)
col3.metric("Min temperature", min_temp)
col4.metric("Max precipitation", max_precipitation)
col5.metric("Average risk", avg_risk)
####

@st.cache_data
def load_data():
    query = text("""
        SELECT
            c.city_name,
            w.forecast_date,
            w.temperature_max,
            w.temperature_min,
            w.precipitation,
            w.wind_speed_max,
            w.wind_gust_max,
            r.risk_score,
            r.risk_level,
            r.rain_risk,
            r.wind_risk,
            r.temperature_risk,
            r.weather_code_risk
        FROM weatherforecasts w
        JOIN cities c
            ON w.city_id = c.id
        JOIN risks r
            ON r.forecast_id = w.forecast_id
        ORDER BY w.forecast_date
    """)
    return pd.read_sql(query, engine)

data = load_data()
data["forecast_date"] = pd.to_datetime(data["forecast_date"])


###




st.subheader(
"Risk factors"
)

risk_city = st.selectbox(
    "Analyze risk factors for",
    sorted(data["city_name"].unique())
    )

city_risk_data = data[
    data["city_name"] == risk_city
    ]




st.subheader(f"{risk_city} Summary")

city_col1, city_col2, city_col3 = st.columns(3)

city_avg_risk = city_risk_data["risk_score"].mean()

city_max_risk = city_risk_data["risk_score"].max()

city_risk_level = (city_risk_data["risk_level"].mode())

city_rain_risk= data["rain_risk"].mean()

city_wind_risk= data["wind_risk"].mean()

city_weather_code_risk=data["weather_code_risk"].mean()


city_col1.metric(
"Average risk score",
round(city_avg_risk, 2)
)

city_col2.metric(
"Maximum risk score",
round(city_max_risk, 2)
)

city_col3.metric(
"Most common risk level",
city_risk_level
)







###
cities = pd.read_sql(
    "SELECT city_name FROM cities ORDER BY city_name",
    engine
)



selected_cities = st.multiselect(
    "select cities",
    cities["city_name"].tolist()
)



dates = pd.read_sql(
    """
    SELECT forecast_date
    FROM weatherforecasts
    WHERE forecast_date IS NOT NULL
	group by forecast_date
    ORDER BY forecast_date
    """,
    engine
)

dates["forecast_date"] = pd.to_datetime(
    dates["forecast_date"],
    errors="coerce"
)


min_date = dates["forecast_date"].min().date()
max_date = dates["forecast_date"].max().date()

selected_dates = st.date_input(
    "Select period",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)



risk_lvl = pd.read_sql(
    "SELECT risk_level FROM risks GROUP BY(risk_level)",
    engine
)

selected_risk_lvl = st.selectbox(
    "select a risk",
    ["all risk"] + risk_lvl["risk_level"].tolist()
)


if selected_cities:
    data = data[data["city_name"].isin(selected_cities)]


if len(selected_dates) == 2:
    start_date, end_date = selected_dates

    data = data[
        (data["forecast_date"].dt.date >= start_date) &
        (data["forecast_date"].dt.date <= end_date)
    ]


if selected_risk_lvl != "all risk":
    data = data[data["risk_level"] == selected_risk_lvl]

if data.empty:
    st.warning("No data matches the selected filters.")
    st.stop()




#charts

###highest 10 cities by temps
st.subheader("top villes temperatures les plus elevees")

top_10_temperature = (
    data.groupby("city_name")["temperature_max"]
    .max()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_10_temperature,height=450)

###

st.subheader("top villes precipitation les plus elevees")

top_10_precipitation = (
    data.groupby("city_name")["precipitation"]
    .max()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_10_precipitation,height=450)

###top 
st.subheader("Top highest average risk cities")

top_risk_cities = (
    data.groupby("city_name")["risk_score"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_risk_cities)
###risk evolution

st.subheader("Risk score over time")

risk_by_date = (
    data.groupby("forecast_date")["risk_score"]
    .mean()
)

st.line_chart(risk_by_date, height=400)



###
st.subheader("Risk by city and date")

risk_scatter = data.copy()

st.scatter_chart(
    risk_scatter,
    x="forecast_date",
    y="risk_score",
    color="city_name",
    size="risk_score",
    height=500
)

##

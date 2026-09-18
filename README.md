# Weather Risk Pipeline

A data engineering project that collects, transforms, analyzes, and visualizes weather forecast data for cities in Morocco.

The pipeline uses **Open-Meteo** as the weather data source and follows a **Bronze → Silver → Gold** architecture. **Apache Airflow** orchestrates the pipeline, **PostgreSQL** stores the processed data, and **Streamlit** provides an interactive dashboard for weather risk analysis.

## Project Objectives

* Collect weather forecasts for Moroccan cities.
* Clean and transform the collected data.
* Calculate weather risk scores based on precipitation, wind, temperature, and weather conditions.
* Store the processed data in PostgreSQL.
* Analyze weather risks by city and date.
* Visualize the results through an interactive Streamlit dashboard.

## API and Technologies

### Weather API

The project uses the **Open-Meteo API** to retrieve weather forecasts.

The pipeline collects:

* Maximum and minimum temperature
* Precipitation
* Precipitation probability
* Maximum wind speed
* Maximum wind gusts
* Weather codes
* Forecast dates

### Technologies

* **Python** — data processing and pipeline development
* **Pandas** — data cleaning and transformation
* **SQLAlchemy** — database interaction
* **PostgreSQL** — data storage
* **Apache Airflow** — pipeline orchestration
* **Streamlit** — interactive dashboard
* **Docker / Docker Compose** — containerization
* **Open-Meteo** — weather data source
* **Git / GitHub** — version control

## Project Architecture

The pipeline follows a **Bronze → Silver → Gold** architecture:

```text
                    Open-Meteo API
                          │
                          ▼
                    ┌───────────┐
                    │  Bronze   │
                    │ Raw data  │
                    └─────┬─────┘
                          │
                          ▼
                    ┌───────────┐
                    │  Silver   │
                    │ Clean data│
                    └─────┬─────┘
                          │
                          ▼
                    ┌───────────┐
                    │   Gold    │
                    │ Risk data │
                    └─────┬─────┘
                          │
                          ▼
                     PostgreSQL
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
        Airflow DAG               Streamlit
        Orchestration             Dashboard
```

### Pipeline Layers

**Bronze**

Contains the raw data extracted from the weather API before transformation.

**Silver**

Contains cleaned and structured weather data ready for analysis.

**Gold**

Contains the processed weather data with calculated risk indicators, risk scores, and risk levels.

The pipeline is orchestrated with **Apache Airflow**, and the final data is stored in **PostgreSQL** for analysis and visualization.

## Project Structure

```text
weather-risk-pipeline/
│
├── extraction/
│   ├── extract.py
│   └── ma.csv
│
├── transformation/
│   ├── transform.py
│   └── feature_engineering.py
│
├── load/
│   ├── database.py
│   ├── models.py
│   ├── create_tables.py
│   ├── load_cities.py
│   ├── load_weather.py
│   └── load_risks.py
│
├── dags/
│   └── weather_pipeline.py
│
├── bronze/
│   └── .gitkeep
│
├── silver/
│   └── .gitkeep
│
├── gold/
│   └── weather_gold.csv
│
├── sql/
│   ├── schema.sql
│   └── analysis.sql
│
├── streamlit_app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

The **Streamlit dashboard** is implemented in `streamlit_app.py`.

## Installation and Execution

### 1. Clone the repository

```bash
git clone <repository-url>
cd weather-risk-pipeline
```

### 2. Install dependencies

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file containing the PostgreSQL database configuration required by the project.

### 4. Run with Docker Compose

Build and start the services:

```bash
docker compose up --build
```

The project provides:

* **Airflow:** `http://localhost:8081`
* **Streamlit Dashboard:** `http://localhost:8501`

### 5. Stop the services

```bash
docker compose down
```

## Database Schema

The project uses **PostgreSQL** to store the processed weather data.

The database contains three main tables:

### `cities`

Stores information about the Moroccan cities used by the pipeline.

| Column      | Description                   |
| ----------- | ----------------------------- |
| `id`        | Unique identifier of the city |
| `city_name` | Name of the city              |
| `latitude`  | Geographic latitude           |
| `longitude` | Geographic longitude          |

### `weatherforecasts`

Stores the weather forecast for each city and date.

| Column                      | Description                               |
| --------------------------- | ----------------------------------------- |
| `forecast_id`               | Unique identifier of the forecast         |
| `city_id`                   | Reference to the city                     |
| `forecast_date`             | Date of the forecast                      |
| `temperature_max`           | Maximum temperature                       |
| `temperature_min`           | Minimum temperature                       |
| `precipitation`             | Expected precipitation                    |
| `precipitation_probability` | Probability of precipitation              |
| `wind_speed_max`            | Maximum wind speed                        |
| `wind_gust_max`             | Maximum wind gust                         |
| `weather_code`              | Open-Meteo weather code                   |
| `retrieved_at`              | Date and time when the data was retrieved |

A unique constraint on `city_id` and `forecast_date` prevents duplicate forecasts for the same city and date.

### `risks`

Stores the weather risk calculated from each forecast.

| Column              | Description                                    |
| ------------------- | ---------------------------------------------- |
| `risk_id`           | Unique identifier of the risk                  |
| `forecast_id`       | Reference to the corresponding forecast        |
| `rain_risk`         | Risk related to precipitation                  |
| `wind_risk`         | Risk related to wind                           |
| `temperature_risk`  | Risk related to temperature                    |
| `weather_code_risk` | Risk related to weather conditions             |
| `risk_score`        | Overall calculated risk score                  |
| `risk_level`        | Risk category: Low, Moderate, High, or Extreme |

### Relationships

```text
cities
  │
  │ 1
  │
  │ N
  ▼
weatherforecasts
  │
  │ 1
  │
  │ 1
  ▼
risks
```

* One city can have many weather forecasts.
* Each weather forecast belongs to one city.
* Each weather forecast has one corresponding risk record.

## Dashboard

The project includes an interactive **Streamlit dashboard** for exploring weather conditions and risk levels across Moroccan cities.

The dashboard provides:

* Key weather indicators
* Top 10 cities by maximum temperature
* Top 10 highest-risk cities
* Average risk evolution over time
* Risk by city and date
* Top 10 highest-risk dates
* Filters by city, date range, and risk level

The dashboard can be launched with:

```bash
docker compose up --build
```

Then open:

```text
http://localhost:8501
```

## Airflow Pipeline

The data pipeline is orchestrated using **Apache Airflow**.

The DAG is located in:

```text
dags/weather_pipeline.py
```

The pipeline executes the main data processing steps in sequence:

```text
Extract
   ↓
Transform
   ↓
Feature Engineering
   ↓
Load
```

### Pipeline Steps

1. **Extract** — Retrieves weather forecast data from Open-Meteo.
2. **Transform** — Cleans and prepares the raw weather data.
3. **Feature Engineering** — Calculates weather risk indicators, risk scores, and risk levels.
4. **Load** — Stores the processed data in PostgreSQL.

Airflow is responsible for scheduling and monitoring the execution of these tasks.

The Airflow interface is available at:

```text
http://localhost:8081
```

## Dependencies

The main Python dependencies used by the project are listed in `requirements.txt`.

They include libraries for:

* Data extraction and HTTP requests
* Data processing with Pandas
* Database access with SQLAlchemy and PostgreSQL
* Airflow pipeline orchestration
* Streamlit dashboard development
* Environment variable management

Install all dependencies with:

```bash
pip install -r requirements.txt
```

## UML Diagram

The following UML diagram represents the main entities used in the weather risk data model and their relationships.

The model contains three main entities:

* **City** — stores information about Moroccan cities.
* **WeatherForecast** — stores weather forecasts associated with cities.
* **Risk** — stores the risk analysis associated with each forecast.

```text
┌─────────────────────────┐
│          City           │
├─────────────────────────┤
│ id                      │
│ city_name               │
│ latitude                │
│ longitude               │
└────────────┬────────────┘
             │
             │ 1
             │
             │ *
             ▼
┌─────────────────────────┐
│    WeatherForecast      │
├─────────────────────────┤
│ forecast_id             │
│ city_id                 │
│ forecast_date           │
│ temperature_max         │
│ temperature_min         │
│ precipitation           │
│ precipitation_probability│
│ wind_speed_max          │
│ wind_gust_max           │
│ weather_code            │
│ retrieved_at            │
└────────────┬────────────┘
             │
             │ 1
             │
             │ 1
             ▼
┌─────────────────────────┐
│          Risk           │
├─────────────────────────┤
│ risk_id                 │
│ forecast_id             │
│ rain_risk               │
│ wind_risk               │
│ temperature_risk        │
│ weather_code_risk       │
│ risk_score              │
│ risk_level              │
└─────────────────────────┘
```

The complete data model is implemented using SQLAlchemy in `load/models.py`.

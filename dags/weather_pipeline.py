from airflow import DAG
from extraction.extract import extract
from transformation.transform import transform
from transformation.feature_engineering import feature
from load.load_weather import load_weather
from load.load_risks import load_risks
from load.load_cities import load_cities
from datetime import datetime
from airflow.operators.python import PythonOperator
from load.create_tables import create_tables



dag = DAG(
    dag_id="weather_pipeline",
    start_date=datetime(2026, 9, 15),
    schedule="@daily", 
    catchup=False,
    max_active_runs=1
)

create_tables_task = PythonOperator(
    task_id="create_tables",
    python_callable=create_tables,
    dag=dag
)



extract_task = PythonOperator(
        task_id="execute_extract",
        python_callable=extract,
        dag=dag
    )

load_cities_task = PythonOperator(
        task_id="execute_load_cities",
        python_callable=load_cities,
        dag=dag
    )

transform_task = PythonOperator(
        task_id="execute_transform",
        python_callable=transform,
        dag=dag
    )
feature_task = PythonOperator(
        task_id="execute_feature",
        python_callable=feature,
        dag=dag
    )
load_weather_task = PythonOperator(
        task_id="execute_load_weather",
        python_callable=load_weather,
        dag=dag
    )


load_risk_task = PythonOperator(
        task_id="execute_load_risk",
        python_callable=load_risks,
        dag=dag
    )

create_tables_task >> extract_task >> load_cities_task >> transform_task >> feature_task >> load_weather_task >> load_risk_task